from django.urls import path
from .views import NewsListCreateView , NewsDetailView

urlpatterns = [
    path('',NewsListCreateView.as_view() , name='new_list_create'),
    path('<int:pk>/',NewsDetailView.as_view() , name='new_detail'),

]