from django.db import models
from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
from backend_test.utils.constants import UNIT_LABELS


# TODO here we can add any field you need in order to be scalable
class Employee(User):
    slack_id = models.CharField(max_length=100)


class Meal(models.Model):
    name = models.CharField(max_length=50)
    unit_cost = models.PositiveIntegerField()
    unit_label = models.CharField(max_length=4, choices=UNIT_LABELS)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Combination(models.Model):
    meals = models.ManyToManyField(Meal)
    description = models.TextField()

    def __str__(self):
        return self.description


class Menu(models.Model):
    date = models.DateField()
    combinations = models.ManyToManyField(Combination)

    def __str__(self):
        return str(self.date)


class Order(models.Model):
    owner = models.ForeignKey(Employee, on_delete=models.CASCADE)
    combination = models.ForeignKey(Combination, on_delete=models.CASCADE)
    comments = models.TextField(blank=True)
