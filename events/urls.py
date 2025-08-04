from django.urls import path
from .views import EventListCreateView , EventDetailView , RegisterEventView

urlpatterns = [
    path('',EventListCreateView.as_view() , name='event_list_create'),
    path('<int:pk>/',EventDetailView.as_view() , name='event_detail'),
    path('<int:pk>/register/',RegisterEventView.as_view() , name='event_register'),
]