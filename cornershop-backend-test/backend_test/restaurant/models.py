from django.db import models
from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
from backend_test.utils.constants import UNIT_LABELS


# TODO here we can add any field you need in order to be scalable
class CustomUser(User):
    name = models.CharField(max_length=30)


class Meal(models.Model):
    name = models.CharField(max_length=50)
    unit_label = models.CharField(max_length=4, choices=UNIT_LABELS)
    stock = models.PositiveIntegerField(default=0)


class Menu(models.Model):
    date = models.DateField(auto_now=True)
    meals = models.ManyToManyField(Meal)
    description = models.TextField()


class Order(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
