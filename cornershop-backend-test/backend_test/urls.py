"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import include

from .restaurant.views import *


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('auth/', include('rest_auth.urls')),
   path('restaurant/', include('backend_test.restaurant.urls')),
   path('views/login', login, name='login'),
   path('views/meal', meal, name='meal'),
   path('views/combination', combination, name='combination'),
   path('views/menu', menu, name='menu'),
   re_path(r'views/menu/(?P<uuid>[a-z0-9]+)/$', menu, name='menu_detail')
]

