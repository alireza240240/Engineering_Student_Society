from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_short', 'author', 'created_at', 'article', 'news', 'event')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username')

    def content_short(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_short.short_description = 'Content'