from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .permissions import IsAdmin
from .models import Article
from .serializers import ArticleSerializer

# articl_list_create     get==HAME , post == HAME
# my_article  ISAUTH -> get== khodAuthor , admin 
# article_detail get=HAME artc ke approve bsh mibinn --- put if request.user == author or request.user.role == 'admin'
# article

class ArticleListCreateView(APIView):

    def get(self,request):
        articles = Article.objects.filter(status='approved')
        serializer = ArticleSerializer(articles , many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = ArticleSerializer(data=request.data) # ststus nmtn chng readonl hast
        if serializer.is_valid():
            serializer.save(author=request.user)
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

        # if request.user == article.author or request.user.role == 'admin' :
        if request.user == article.author :
            serializer = ArticleSerializer(article,data=request.data)
            if serializer.is_valid():
                serializer.save() # inja byd admin ro hzf konam ke save nshe kt_52 # khb alan khondam ke lazm ham nis chon virayesh va ndi hamon author ghbli mishe ke alie # (author=request.user)
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
        # in else ke agar req.usr hamon auth nabood gzshtm ke nbsh None mide



class MyArticlesView(APIView): # bry inke hame chnta artcl har authr bbine to detail yedone mal khdsh ro midid inja hme artcl mal khdsh
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


    

