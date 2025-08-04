from rest_framework import serializers
from .models import Event, EventParticipant

class EventSeializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(read_only = True)
    spots_left = serializers.ReadOnlyField() 
        
    class Meta:
        model = Event
        fields = ['id','title','description','date','created_at','creator','capacity','spots_left']

class RegisterEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = ['event']