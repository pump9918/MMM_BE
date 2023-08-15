from django.contrib import admin
from .models import Post, TTSAudio, TTSAudioTitle, Like

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    pass

@admin.register(TTSAudioTitle)
class PostModelAdmin(admin.ModelAdmin):
    pass

@admin.register(TTSAudio)
class PostModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'timestamp')
    list_filter = ('user', 'post', 'timestamp')