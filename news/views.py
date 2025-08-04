from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .serializers import NewsSerializer
from .models import News
from core.permissions import IsMemberOrAdmin


class NewsListCreateView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly,IsMemberOrAdmin] 

    def get(self,request):
        news = News.objects.all() # .order_by(-created_at)
        serializer = NewsSerializer(news , many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author = request.user) # byd inja bgi ke author hamoni hast k login krd to serilzr fght gofti to get str in user ro nshn bde to model ham gofti ye news byd dashte bash jayi jz in view tarif nkrdi rah digge in bode to khd serlzr override midrdi context['request'].user middi
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class NewsDetailView(APIView):

    permission_classes =[IsAuthenticatedOrReadOnly , IsMemberOrAdmin]

    def get(self,request,pk):
        news=News.objects.get(pk=pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        news=News.objects.get(pk=pk)
        serializer = NewsSerializer(news,data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        news=News.objects.get(pk=pk)
        news.delete()
        return Response({'message':'pak kardi 😆'},status=status.HTTP_204_NO_CONTENT)