from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from django.http import HttpResponse

from ..utils.components import *

@api_view(['GET', 'HEAD'])
@permission_classes([permissions.AllowAny])
def login(request, *args, **kwargs):
    fields = ({'id': 'username', 'label': 'Username', 'type': 'text'},
              {'id': 'password', 'label': 'Password', 'type': 'password'})
    return HttpResponse(f'<html>{h1("Login")}{form("javascript:login()", fields)}{javascript()}</html>', status=200)


@api_view(['GET', 'HEAD'])
# @permission_classes([permissions.IsAdminUser])
def create_meal(request, *args, **kwargs):
    fields = ({'id': 'name', 'label': 'Name', 'type': 'text'},
              {'id': 'unit_label', 'label': 'Unit label', 'type': 'text'},
              {'id': 'stock', 'label': 'Stock', 'type': 'text'})
    return HttpResponse(f'<html>{h1("Create meal")}{form("/restaurant/meal/", fields)}</html>', status=200)


@api_view(['GET', 'HEAD'])
# @permission_classes([permissions.IsAdminUser])
def create_menu(request, *args, **kwargs):
    fields = ({'id': 'date', 'label': 'Date', 'type': 'text'},
              {'id': 'meals', 'label': 'Meals', 'type': 'text'},
              {'id': 'description', 'label': 'Description', 'type': 'text'})
    return HttpResponse(f'<html>{h1("Create menu")}{form("/restaurant/menu/", fields)}</html>', status=200)

