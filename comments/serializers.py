from rest_framework import serializers

from .models import Comment

class CommentSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(read_only=True)

    class Meta :
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'article', 'event' , 'news']
        read_only_fields = ['id', 'author', 'created_at', 'article', 'news', 'event']