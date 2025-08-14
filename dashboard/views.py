from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from articles.permissions import IsAdmin
from articles.models import Article
from events.models import Event
from news.models import News

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



User = get_user_model()

class UserListView(APIView):
   
    permission_classes = [IsAdmin]

    def get(self,request):
        users = User.objects.all().values('id', 'username', 'email', 'role', 'date_joined')
        return Response(list(users),status=status.HTTP_200_OK)
    

class UserRoleUpdateView(APIView):
    def put(self , request , user_id):
        new_role = request.data.get('role')

        valid_roles=['admin','member','normal']
        if not new_role in valid_roles :
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
        
        try :
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user.role = new_role
        user.save()
        return Response({'message': f'Role updated to {new_role} for user {user.username}'}, status=status.HTTP_200_OK)


class UserDeleteView(APIView):

    def delete(self,request, user_id):

        try :
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user == request.user :
            return Response({'error': 'You cannot delete yourself'}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response({'message': f'User {user.username} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

class DashboardSummaryView(APIView):
    permission_classes = [IsAdmin]
    def get(self , request):
        data ={
            "total_users":User.objects.count(),
            "total_members":User.objects.filter(role='member').count(),
            "total_admins":User.objects.filter(role='admin').count(),
            "articles_pending":Article.objects.filter(status='pending').count(),
            "events_upcoming":Event.objects.filter(date__gte=now()).count(),
            "total_articles":Article.objects.count(),
            "total_events":Event.objects.count(),
            "total_news":News.objects.count(),
        }

        return Response(data , status=status.HTTP_200_OK)
    

class PendingArticleView(APIView):
    permission_classes = [IsAdmin]

    def get(self , request):
        articles = Article.objects.filter(status='pending').values(
            'id', 'title', 'author__username', 'created_at'
        )

        return Response(list(articles), status=status.HTTP_200_OK)


class UpcomingEventView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        events = Event.objects.filter(date__gte=now()).values(
            'id', 'title', 'date' , 'capacity'
        )
        return Response(list(events), status=status.HTTP_200_OK)
    

class AllNewsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        news_list = News.objects.all().values(
            'id', 'title', 'author__username', 'created_at'
        )
        return Response(list(news_list), status=status.HTTP_200_OK)