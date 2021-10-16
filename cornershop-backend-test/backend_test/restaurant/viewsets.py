from datetime import datetime

from django.db.models import Q
from rest_framework import permissions
from rest_framework.decorators import permission_classes, action
from rest_framework import viewsets, status
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response

from .models import Employee, Meal, Combination, Menu, Order
from .serializers import EmployeeSerializer, MealSerializer, CombinationSerializer, MenuSerializer, OrderSerializer
from .services import check_date_availability, make_hash
from .tasks import send_slack_reminders


class EmployeeViewSet(viewsets.ModelViewSet):
    model = Employee
    queryset = model.objects.all()
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a new user, also adds the extended fields
        @request.data : DICT {name, username, password, slack_id}
        """
        data = request.data
        employee = Employee.objects.create(first_name=data['name'], username=data['username'],
                                           password=make_password(data['password']), slack_id=data['slack_id'])
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Only allows creation
    def list(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


@permission_classes([permissions.IsAdminUser])
class MealViewSet(viewsets.ModelViewSet):
    model = Meal
    queryset = model.objects.all()
    serializer_class = MealSerializer

    @action(detail=False, methods=['post'])
    def update_stock(self, request):
        for data in request.data:
            meal = Meal.objects.get(id=data['id'])
            meal.stock = data['stock']
            meal.save()
        return Response(request.data, status=status.HTTP_200_OK)


@permission_classes([permissions.IsAdminUser])
class CombinationViewSet(viewsets.ModelViewSet):
    model = Combination
    queryset = model.objects.all()
    serializer_class = CombinationSerializer


@permission_classes([permissions.IsAdminUser])
class MenuViewSet(viewsets.ModelViewSet):
    model = Menu
    queryset = model.objects.all()
    serializer_class = MenuSerializer

    def create(self, request, *args, **kwargs):
        """
        Verify if the date is available to create the new menu.
        """
        data = request.data
        if check_date_availability(data['date']):
            menu = Menu.objects.create(date=data['date'], uuid=make_hash(data['date']))
            menu.combinations.add(*data['combinations'])
            serializer = MenuSerializer(menu)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message': f'Date {data["date"]} is already used'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Checks if the field date won't be updated, otherwise checks availability to perform creation.
        """
        data = request.data
        if 'date' not in data or check_date_availability(int(kwargs['pk']), data['date']):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            data['uuid'] = make_hash(instance.date)
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': f'Date {data["date"]} is already used'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def send_reminders(self, request):
        send_slack_reminders.delay(request.data['id'])
        return Response({'status': 'Working'}, status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
class OrderViewSet(viewsets.ModelViewSet):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Creation intercepted to verify due date or resubmission
        """
        data = request.data
        owner = Employee.objects.get(id=request.user.id)
        menu = Menu.objects.get(id=data['menu'])
        combination = Combination.objects.get(id=data['combination'])
        if menu.date.day == datetime.today().day and datetime.now().hour >= 11:
            return Response({'message': 'Time expired. The menu is closed'}, status=status.HTTP_400_BAD_REQUEST)
        elif combination not in menu.combinations.all():
            # In case that the request is sent by other side and data don't match
            return Response({'message': f'The combination {combination.id} is not in menu {menu.id}'},
                            status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.filter(Q(owner=owner) and Q(menu=menu)).first()
        if not order:
            order = Order.objects.create(
                owner=owner, menu=menu, combination=combination, observations=data['observations'])
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:  # Should use update method, but for reuse in front
            for meal in order.combination.meals.all():
                #  Restores stock
                meal.stock += meal.unit_cost
                meal.save()
            order.combination = combination
            # if 'observations' in data:
            order.observations = data['observations']
            order.save()
        for meal in order.combination.meals.all():
            meal.stock -= meal.unit_cost
            meal.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
