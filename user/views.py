
from rest_framework import generics
from rest_framework.generics import ListAPIView
from .serializers import  ProfileSerializer, EditorProfileSerializer
from .models import Profile, EditorProfile
from posts.models import Post
from posts.serializers import PostSerializer


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    

class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Profile.objects.all()
    # serializer_class = ProfileSerializer

    # def get_queryset(self):
    #     return Profile.objects.filter(user=self.request.user)
    
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()  # Use this instead of get_queryset()

    def get_object(self):
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)
        return profile
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    
class UserPostsListView(ListAPIView): #로그인한 유저가 작성한 게시물 모아보기
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = []

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)
    
class LikedPostsListView(generics.ListAPIView): #로그인한 유저가 좋아요 누른 게시물 모아보기
    serializer_class = PostSerializer
    permission_classes = []

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(like__user=user)

    
class EditorProfileView(generics.GenericAPIView):
    queryset  = EditorProfile.objects.all()
    serializer_class = EditorProfileSerializer