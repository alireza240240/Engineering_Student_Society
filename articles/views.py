from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly
from rest_framework import status

from .permissions import IsAdmin
from .models import Article
from .serializers import ArticleSerializer

from .tasks import notify_admin_new_article


class ArticleListCreateView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]  
    def get(self,request):
        articles = Article.objects.filter(status='approved')
        serializer = ArticleSerializer(articles , many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = ArticleSerializer(data=request.data) 
        if serializer.is_valid():

            article = serializer.save(author=request.user)
            notify_admin_new_article.delay(article.title, request.user.username)

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):

    permission_classes= [IsAuthenticated]

    def get(self,request,pk):
        try :
            article = Article.objects.get(pk = pk)
        except Article.DoesNotExist:
            return Response({"error": "Article Not Found ... 🍒"},status=status.HTTP_404_NOT_FOUND)

        if article.status == 'approved' or request.user == article.author or request.user.role == 'admin' :
            serializer = ArticleSerializer(article)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else :
            return Response({'error':'OOps You Dont Have Permission To See This Article ...🍋'})

 
    def put(self,request,pk):
        try :
            article = Article.objects.get(pk = pk)
        except Article.DoesNotExist:
            return Response({'error': 'Article Not Found ... 🍒'},status=status.HTTP_404_NOT_FOUND)


        if request.user == article.author :
            serializer = ArticleSerializer(article,data=request.data)
            if serializer.is_valid():
                serializer.save() 
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'error':'OOps You Dont Have Permission For Update Data ...🍋'})
        
    def delete(self,request,pk):

        try :
            article = Article.objects.get(pk = pk)
        except Article.DoesNotExist:
            return Response({'error': 'Article Not Found ... 🍒'},status=status.HTTP_404_NOT_FOUND)

        if request.user == article.author :
            article.delete()
            return Response({'message':'pak kardi Article ro 😆'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'OOps You Dont Have Permission For Delete Data ...🍋'})



class MyArticlesView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self,request):
        articles = Article.objects.filter(author=request.user)
        serializer = ArticleSerializer(articles , many = True)
        return Response (serializer.data , status=status.HTTP_200_OK)



class ApproveArticleView(APIView):
    permission_classes=[IsAdmin]

    def put(self,request,pk):

        try :
            article = Article.objects.get(pk = pk)
            article.status = 'approved'
            article.save()
            return Response({"message":"This Article Now Is Approved ...🍋 "})
        except Article.DoesNotExist:
            return Response({'error': 'Article Not Found ... 🍒'},status=status.HTTP_404_NOT_FOUND)


class RejectArticleView(APIView):
    permission_classes=[IsAdmin]

    def put(self,request,pk):

        try :
            article = Article.objects.get(pk = pk)
            article.status = 'rejected'
            article.save()
            return Response({"message":"Ooops Article Rejected ...🍓 "})
        except Article.DoesNotExist:
            return Response({'error': 'Article Not Found ... 🍒'},status=status.HTTP_404_NOT_FOUND)


    

