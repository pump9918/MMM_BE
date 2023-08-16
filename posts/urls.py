from django.urls import path
from rest_framework import routers

from .views import PostViewSet, TTSAudioAPIView, TTSAudioTitleAPIView, EditorPostViewSet

router = routers.SimpleRouter()
router.register('posts', PostViewSet)
# router.register('editorposts', EditorPostViewSet)

router.register('editorposts', EditorPostViewSet, basename='editorposts')

# urlpatterns = router.urls
urlpatterns = [
    *router.urls,
    path('posts/<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('posts/<int:pk>/tts_title_mp3/', TTSAudioTitleAPIView.as_view(), name='tts_title_mp3'),
    path('posts/<int:pk>/tts_mp3/', TTSAudioAPIView.as_view(), name='tts-audio-api'),
    path('editorposts/top3/', EditorPostViewSet.as_view({'get': 'top3'}), name='editorpost-top3'),
    path('editorposts/<int:pk>/update/', EditorPostViewSet.as_view({'put': 'update_post'}), name='editor-post-update'),
    path('editorposts/<int:pk>/delete/', EditorPostViewSet.as_view({'delete': 'delete_post'}), name='editor-post-delete'),
]
    
