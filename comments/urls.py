from django.urls import path
from .views import ArticleCommentsView, NewsCommentsView, EventCommentsView

urlpatterns = [
    path('articles/<int:article_id>/' , ArticleCommentsView.as_view() , name='article_comments'),
    path('news/<int:news_id>/' , NewsCommentsView.as_view() , name='news_comments'),
    path('events/<int:event_id>/' , EventCommentsView.as_view() , name='event_comments'),
]