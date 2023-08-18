from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from user.models import User, EditorProfile


#게시물 제목 tts 파일
class TTSAudioTitle(models.Model):
    title_message = models.TextField()
    audio_file = models.FileField(upload_to='tts_title/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 유저 모델 연결

    def __str__(self):
        return self.title_message

#게시물 tts 파일
class TTSAudio(models.Model):
    message = models.TextField()
    audio_file = models.FileField(upload_to='tts/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 유저 모델 연결

    def __str__(self):
        return self.message


class Post(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_nickname')
    # like = models.ManyToManyField(User, related_name='liked_post', blank=True, default=0)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_posts')
    published_date = models.DateTimeField(default=timezone.now)
    tts_title_audio = models.ForeignKey(TTSAudioTitle, on_delete=models.SET_NULL, null=True, blank=True)
    tts_audio = models.ForeignKey(TTSAudio, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='post/', blank=True, null=True, default = '')
    due_date = models.DateTimeField(blank=True, null=True) #마감일
    event_date = models.DateTimeField(blank=True, null=True) #행사 날짜
    

    editor_author = models.ForeignKey(EditorProfile, on_delete=models.CASCADE, related_name='editorprofile_name')
    
    editor_name = models.CharField(max_length=20, blank=False, null=False, default='')
    phonenum = models.CharField(max_length=20, blank=True, null=True) #전화번호
    editor_address = models.CharField(max_length=50, blank=False, null=False, default='')
    def __str__(self):
        return self.title
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')