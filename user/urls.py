from django.urls import path
from .views import ProfileListView, ProfileView, EditorProfileView, UserPostsListView, LikedPostsListView

app_name = 'users'

urlpatterns = [
    path('', ProfileListView.as_view()),
    path('<int:pk>/', ProfileView.as_view()),
    path('editorprofile/<int:pk>/', EditorProfileView.as_view()),
    path('current-user-posts/', UserPostsListView.as_view(), name='user-posts-list'),
    path('liked-posts/', LikedPostsListView.as_view(), name='liked-posts-list'),
]