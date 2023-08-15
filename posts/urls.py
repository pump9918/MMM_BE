from django.urls import path
from rest_framework import routers

from .views import PostViewSet, TTSAudioAPIView, TTSAudioTitleAPIView

router = routers.SimpleRouter()
router.register('posts', PostViewSet)
# router.register('editorposts', EditorPostViewSet)


# urlpatterns = router.urls
urlpatterns = [
    *router.urls,
    path('posts/<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('posts/<int:pk>/tts_title_mp3/', TTSAudioTitleAPIView.as_view(), name='tts_title_mp3'),
    path('posts/<int:pk>/tts_mp3/', TTSAudioAPIView.as_view(), name='tts-audio-api'),
]