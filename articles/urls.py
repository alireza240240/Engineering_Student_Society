from django.urls import path
from .views import (ArticleListCreateView ,
                    ArticleDetailView ,
                    MyArticlesView ,
                    ApproveArticleView ,
                    RejectArticleView)

urlpatterns = [
    path('',ArticleListCreateView.as_view(),name='article_list_create'),
    path('<int:pk>/',ArticleDetailView.as_view(),name='article_detail'),
    path('my/',MyArticlesView.as_view(),name='my_article'),
    path('<int:pk>/approve/',ApproveArticleView.as_view(),name='article_approve'),
    path('<int:pk>/reject/',RejectArticleView.as_view(),name='article_reject'),

]

