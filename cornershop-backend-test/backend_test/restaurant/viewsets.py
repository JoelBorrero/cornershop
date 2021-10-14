from rest_framework import permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import viewsets, status
from django.http import HttpResponse
from rest_framework.response import Response

from .models import *
from .serializers import *


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    model = Meal

    # @api_view(["GET", "HEAD"])
    @permission_classes([permissions.IsAdminUser])
    def create(self, request, *args, **kwargs):
        meal = Meal.objects.create(name=request.data['name'], unit_label=request.data['unit_label'],
                                   stock=request.data['stock'])
        return Response(MealSerializer(meal).data, status=201)

