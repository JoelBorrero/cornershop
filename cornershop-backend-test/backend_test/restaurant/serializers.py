from rest_framework import serializers
from .models import Employee, Meal, Combination, Menu


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'username', 'slack_id']


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'name', 'unit_cost', 'unit_label', 'stock']


class CombinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combination
        fields = ['id', 'meals', 'description']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'date', 'combinations']
