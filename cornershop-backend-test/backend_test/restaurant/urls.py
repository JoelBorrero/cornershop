from django.urls import path, include
from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()
router.register('employee', viewsets.EmployeeViewSet, basename='employee')
router.register('meal', viewsets.MealViewSet, basename='meal')
router.register('combination', viewsets.CombinationViewSet, basename='combination')
router.register('menu', viewsets.MenuViewSet, basename='menu')


urlpatterns = [
    path(r'', include(router.urls))
]