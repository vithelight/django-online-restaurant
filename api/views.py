from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import serializers
from rest import models


@api_view(['GET'])
def getData(req):
  foods = models.Food.objects.all()
  serializer = serializers.FoodSerializer(foods, many=True)
  return Response(serializer.data)
