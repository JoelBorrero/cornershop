from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from django.http import HttpResponse
from django.template import loader

from ..utils.constants import *
from .models import Meal, Combination, Menu, Order
from .serializers import MealSerializer, CombinationSerializer, MenuSerializer, MenuSerializerDeep
from .services import get_menus_info


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
    # List intercepted to show name instead of id
    # for menu in menu_items:
    #     for index, combination in enumerate(menu['combinations']):
    #         menu['combinations'][index] = Meal.objects.filter(id=combination).first().name
    template = loader.get_template('combination.html')
    document = template.render({'meals': meal_items, 'fields': COMBINATION_FIELDS, 'table': menu_items})
    return HttpResponse(document, status=200)


@api_view(['GET', 'HEAD'])
# @permission_classes([permissions.IsAuthenticated])
def menu(request, *args, **kwargs):
    """
    This view is restricted to only authenticated users.
    For admin allows the visualization and creation of all meals menus.
    For users allows the selection of their preferred option.
    """
    if request.user.is_superuser:
        if 'uuid' in kwargs:
            menu = Menu.objects.get(uuid=kwargs['uuid'])
            serializer = MenuSerializerDeep(menu).data
            for combination in serializer['combinations']:
                # order = Order.objects.filter(Q(combination=combination['id']) & Q(menu=menu.id))
                order = Order.objects.filter(combination=combination['id']).filter(menu=menu.id)
                combination['requests'] = [{'owner': o.owner.first_name, 'observations': o.observations}
                                           for o in order]
            template = loader.get_template('menu_detail_admin.html')
            document = template.render({'menu': serializer})
        else:
            menus_list = Menu.objects.order_by('date')
            # Parses OrderedDict into Dict objects
            menu_items = [dict(m) for m in MenuSerializer(menus_list, many=True).data]
            combinations_list = Combination.objects.all()
            combination_items = CombinationSerializer(combinations_list, many=True).data
            # List intercepted to show name instead of id
            for menu in menu_items:
                for index, combination in enumerate(menu['combinations']):
                    menu['combinations'][index] = ', '.join(
                        [meal.name for meal in Combination.objects.get(id=combination).meals.all()])
            template = loader.get_template('menu_admin.html')
            document = template.render({'combinations': combination_items, 'fields': MENU_FIELDS, 'table': menu_items})
    elif request.user.is_authenticated and 'id' not in kwargs:
        submittable, today_menu, next_menu = get_menus_info()
        template = loader.get_template('menu.html')
        document = template.render({'today_menu': today_menu, 'next_menu': next_menu, 'submittable': submittable})
    else:
        menu = Menu.objects.get(uuid=kwargs['uuid'])
        document = f'<h1>{menu.date}</h1>'
    return HttpResponse(document, status=200)
