from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .models import Comment
from .serializers import CommentSerializer
from news.models import News
from articles.models import Article
from events.models import Event


class ArticleCommentsView(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self , request , article_id):
        comments = Comment.objects.filter(article_id = article_id).order_by('-created_at')
        serializer = CommentSerializer(comments , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def post(self , request , article_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author =request.user , article_id=article_id)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)



class EventCommentsView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self , request , event_id):
        comments = Comment.objects.filter(event_id = event_id).order_by('-created_at')
        serializer = CommentSerializer(comments , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def post(self , request , event_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author =request.user , event_id=event_id)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class NewsCommentsView(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self , request , news_id):
        comments = Comment.objects.filter(news_id = news_id).order_by('-created_at')
        serializer = CommentSerializer(comments , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def post(self , request , news_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author =request.user , news_id=news_id)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
