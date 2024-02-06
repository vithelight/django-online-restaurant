from rest_framework import serializers
from rest import models

class FoodSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Food
    fields = '__all__'

