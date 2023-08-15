from django.urls import path
from .views import UserListView, UserView, UserPostsListView, LikedPostsListView

app_name = 'user'

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserView.as_view()),
    path('current-user-posts/', UserPostsListView.as_view(), name='user-posts-list'),
    path('liked-posts/', LikedPostsListView.as_view(), name='liked-posts-list'),
]