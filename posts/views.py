from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
# from .permissions import CustomReadOnly
from user.models import User
from .models import Post, TTSAudioTitle, TTSAudio, Like
from .serializers import PostSerializer
from .paginations import PostPagination

#tts 관련
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = []
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ["author"] # 이름으로 게시물 모아보기
    search_fields = ["author"]
    ordering_fields = ["published_date"] #최신 순 정렬
    pagination_class = PostPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PostSerializer
        return PostSerializer
    
    
    def create(self, request, *args, **kwargs):
        return self.create_post_with_audio(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'])
    def create_post_with_audio(self, request):
        print(request.user)
        post_serializer = PostSerializer(data=request.data, context={'request': request})
        if post_serializer.is_valid():
            tts_title_message = request.data.get('tts_title_message')
            tts_message = request.data.get('tts_message')

            existing_tts_title = None
            existing_tts_audio = None

            if tts_title_message:
                try:
                    existing_tts_title = TTSAudioTitle.objects.get(title_message=tts_title_message, user=request.user)
                except TTSAudioTitle.DoesNotExist:
                    pass

            if tts_message:
                try:
                    existing_tts_audio = TTSAudio.objects.get(message=tts_message, user=request.user)
                except TTSAudio.DoesNotExist:
                    pass

            post = post_serializer.save(author=request.user)

            if existing_tts_title:
                post.tts_title_audio = existing_tts_title
            if existing_tts_audio:
                post.tts_audio = existing_tts_audio
            
            post.save()

            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    # def perform_create(self, serializer):
    #     profile = User.objects.get(user=self.request.user)
    #     serializer.save(author=self.request.user, profile=profile)
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            return Response({'message': '좋아요 취소됨'})
        except Like.DoesNotExist:
            Like.objects.create(user=user, post=post)
            return Response({'message': '좋아요 추가됨'})
        

    @action(methods=["GET"], detail=False)
    def top3(self, request):
        queryset = self.get_queryset().annotate(like_count=Count('likes')).order_by("-like_count")[:3]
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
    

        
 # 프론트 서버로 tts_title_mp3파일 전송하기 위한 APIView       
class TTSAudioTitleAPIView(APIView):
    def get(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        if post.tts_title_audio:
            file_path = post.tts_title_audio.audio_file.path
            with open(file_path, 'rb') as f:
                response = HttpResponse(f, content_type='audio/mpeg')
                response['Content-Disposition'] = f'attachment; filename="tts_title_{post.id}.mp3"'
                return response
        return Response({'message': '음성 파일이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
 # 프론트 서버로 tts_mp3파일 전송하기 위한 APIView      
class TTSAudioAPIView(APIView):
    def get(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        if post.tts_audio:
            file_path = post.tts_audio.audio_file.path
            with open(file_path, 'rb') as f:
                response = HttpResponse(f, content_type='audio/mpeg')
                response['Content-Disposition'] = f'attachment; filename="tts_{post.id}.mp3"'
                return response
        return Response({'message': '음성 파일이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        