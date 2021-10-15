from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from django.http import HttpResponse
from django.template import loader

from ..utils.constants import *
from .models import Meal, Combination, Menu
from .serializers import MealSerializer, CombinationSerializer, MenuSerializer
from .services import get_next_menu_info


@api_view(['GET', 'HEAD'])
@permission_classes([permissions.AllowAny])
def login(request, *args, **kwargs):
    """
    This view allows user to login, logout and register. Don't need authentication to see it
    """
    template = loader.get_template('auth.html')
    document = template.render(
        {'login_fields': LOGIN_FIELDS, 'register_fields': REGISTER_FIELDS})
    return HttpResponse(document, status=200)


@api_view(['GET', 'HEAD'])
@permission_classes([permissions.IsAdminUser])
def meal(request, *args, **kwargs):
    """
    This view is restricted to only admin view.
    Allows the visualization and creation of all meals.
    """
    meals_list = Meal.objects.all()
    meal_items = MealSerializer(meals_list, many=True).data
    template = loader.get_template('meal.html')
    document = template.render({'fields': MEAL_FIELDS, 'table': meal_items})
    return HttpResponse(document, status=200)


@api_view(['GET', 'HEAD'])
@permission_classes([permissions.IsAdminUser])
def combination(request, *args, **kwargs):
    """
    This view is restricted to only admin view.
    Allows the visualization and creation of all meals combinations.
    """
    menus_list = Combination.objects.all()
    menu_items = CombinationSerializer(menus_list, many=True).data
    meals_list = Meal.objects.all()
    meal_items = MealSerializer(meals_list, many=True).data
    # List intercepted to show name instead id
    # for menu in menu_items:
    #     for index, combination in enumerate(menu['combinations']):
    #         menu['combinations'][index] = Meal.objects.filter(id=combination).first().name
    template = loader.get_template('combination.html')
    document = template.render({'meals': meal_items, 'fields': COMBINATION_FIELDS, 'table': menu_items})
    return HttpResponse(document, status=200)


@api_view(['GET', 'HEAD'])
# @permission_classes([permissions.IsAdminUser])
@permission_classes([permissions.IsAuthenticated])
def menu(request, *args, **kwargs):
    """
    This view is restricted to only authenticated users.
    For admin allows the visualization and creation of all meals menus.
    For users allows the selection of their preferred option.
    """
    menus_list = Menu.objects.order_by('date')
    menu_items = MenuSerializer(menus_list, many=True).data
    combinations_list = Combination.objects.all()
    combination_items = CombinationSerializer(combinations_list, many=True).data
    if request.user.is_superuser:
        # List intercepted to show name instead id
        # for menu in menu_items:
        #     for index, combination in enumerate(menu['combinations']):
        #         menu['combinations'][index] = Combination.objects.filter(id=combination).first().name
        template = loader.get_template('menu_admin.html')
        document = template.render({'combinations': combination_items, 'fields': MENU_FIELDS, 'table': menu_items})
    else:
        combinations = get_next_menu_info()
        template = loader.get_template('menu.html')
        document = template.render({'combinations': combinations})
    return HttpResponse(document, status=200)
