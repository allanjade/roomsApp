#Serializer is used to convert model/class based content into JSON format
from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from base.models import Room

#serialize the (Room) model content
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
