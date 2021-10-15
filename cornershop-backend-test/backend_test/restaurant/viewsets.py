from rest_framework import permissions
from rest_framework.decorators import permission_classes, action
from rest_framework import viewsets, status
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response

from .models import Employee, Meal, Combination, Menu
from .serializers import EmployeeSerializer, MealSerializer, CombinationSerializer, MenuSerializer
from .services import send_slack_reminders


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


@permission_classes([permissions.IsAdminUser])
class MealViewSet(viewsets.ModelViewSet):
    model = Meal
    queryset = model.objects.all()
    serializer_class = MealSerializer


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

    @action(detail=False, methods=['POST'])
    def send_reminders(self, request):
        send_slack_reminders(request.data['id'])
        return Response({'status': 'Working'}, status=status.HTTP_200_OK)
