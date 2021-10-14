from rest_framework import serializers
from . import models


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Meal
        fields = ['name', 'unit_label', 'stock']