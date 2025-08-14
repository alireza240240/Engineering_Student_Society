from django.urls import path
from .views import UserListView , UserRoleUpdateView , UserDeleteView , DashboardSummaryView , PendingArticleView , UpcomingEventView , AllNewsView

urlpatterns = [
    path('users/',UserListView.as_view() , name='dashboard_user_list'),
    path('users/<int:user_id>/role/',UserRoleUpdateView.as_view() , name='dashboard_user_role_update'),
    path('users/<int:user_id>/delete/',UserDeleteView.as_view() , name='dashboard_user_delete'),
    path('summary/',DashboardSummaryView.as_view() , name='dashboard_summary'),

    path('articles/pending/',PendingArticleView.as_view() , name='dashboard_articles_pending'),
    path('events/upcoming/',UpcomingEventView.as_view() , name='dashboard_events_upcoming'),
    path('news/',AllNewsView.as_view() , name='dashboard_all_news'),
]