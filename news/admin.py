from django.contrib import admin
from .models import News
from django.contrib.admin import ModelAdmin



@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ('title', 'content', 'author', 'created_at')