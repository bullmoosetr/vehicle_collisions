from rest_framework import serializers
from .models import *

class CitiBikeStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitiBikeStation
        fields='__all__' 

class CollisionDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollisionDetail
        fields='__all__' 


class CollisionLocationSerializer(serializers.ModelSerializer):
    collision_detail = CollisionDetailSerializers(read_only=True)

    class Meta:
        model = CollisionLocation
        fields='__all__'   

class BoroughSerializer(serializers.ModelSerializer):
    collision_location = CollisionLocationSerializer(many=True, read_only=True) 
    class Meta:
        model = Borough
        fields='__all__'
