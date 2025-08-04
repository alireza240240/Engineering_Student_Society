from django.contrib import admin

from .models import Event , EventParticipant
from django.contrib.admin import ModelAdmin



@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ('title', 'capacity', 'spots_left' , 'date', 'creator','created_at')


@admin.register(EventParticipant)
class EventParticipantAdmin(ModelAdmin):
    list_display = ('event', 'user' , 'registered_at')

