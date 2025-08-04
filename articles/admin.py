from django.contrib import admin

from .models import Article
from django.contrib.admin import ModelAdmin



@admin.register(Article)
class EventAdmin(ModelAdmin):
    list_display = ('title', 'content', 'status' , 'author','created_at')

