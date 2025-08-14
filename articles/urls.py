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

#  --- git init --- git add . -- git commit -m "" --- git push origin main 
# git remote add origin https://github.com/alireza240240/Engineering_Student_Society.git
# git branch -M main
# git push -u origin main