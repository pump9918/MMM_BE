import os
from gtts import gTTS
from django.conf import settings
from rest_framework import serializers

from user.serializers import ProfileSerializer
from .models import Post, TTSAudio, TTSAudioTitle


class TTSAudioTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TTSAudioTitle
        fields = '__all__'
        
class TTSAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TTSAudio
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.email', read_only=True)
    nickname = ProfileSerializer(read_only=True)
    tts_title_message = serializers.CharField(max_length=100, required=False)
    tts_message = serializers.CharField(max_length=1000, required=False)
    likes = serializers.SerializerMethodField()
    tts_title_audio_message = serializers.CharField(source='tts_title_audio.title_message', read_only=True)
    tts_audio_message = serializers.CharField(source='tts_audio.message', read_only=True)
    
    class Meta:
        # model = Post
        # fields = ('published_date', 'likes', 'author_name', 'title', 'content', 'nickname', 'tts_title_message', 'tts_message', 'tts_title_audio', 'tts_audio', 'tts_title_audio_message', 'tts_audio_message')
        # read_only_fields = ('id', 'published_date', 'likes', 'author', 'nickname')
        model = Post
        fields = ('id', 'published_date', 'likes', 'author_name', 'nickname', 'tts_title_message', 'tts_message', 'tts_title_audio', 'tts_audio', 'tts_title_audio_message', 'tts_audio_message')
        read_only_fields = ('id', 'published_date', 'likes', 'author', 'nickname')

    def create(self, validated_data):
        tts_title_message = validated_data.pop('tts_title_message', None)
        tts_message = validated_data.pop('tts_message', None)
        
        
        author = self.context['request'].user
        
        if tts_title_message: 
            tts_title = gTTS(text=tts_title_message, lang='ko')
            tts_title_audio = TTSAudioTitle(title_message=tts_title_message, user=author)
            tts_title_audio.save()

            tts_folder = os.path.join(settings.MEDIA_ROOT, 'tts_title')
            os.makedirs(tts_folder, exist_ok=True)

            save_path = os.path.join(tts_folder, f'tts_title_{tts_title_audio.id}.mp3')
            tts_title.save(save_path)

            tts_title_audio.audio_file = f'tts_title/tts_title_{tts_title_audio.id}.mp3'
            tts_title_audio.save()

            validated_data['tts_title_audio'] = tts_title_audio
            
        if tts_message:
            tts = gTTS(text=tts_message, lang='ko')
            tts_audio = TTSAudio(message=tts_message, user=author)
            tts_audio.save()

            tts_folder = os.path.join(settings.MEDIA_ROOT, 'tts')
            os.makedirs(tts_folder, exist_ok=True)

            save_path = os.path.join(tts_folder, f'tts_{tts_audio.id}.mp3')
            tts.save(save_path)

            tts_audio.audio_file = f'tts/tts_{tts_audio.id}.mp3'
            tts_audio.save()

            validated_data['tts_audio'] = tts_audio

        post = Post.objects.create(**validated_data)
        return post
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    
    
class EditorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content', 'author', 'likes', 'image', 'published_date')
        read_only_fields = ('likes', 'published_date')

    def create(self, validated_data):
        author = self.context['request'].user
        if author.is_staff:  
            post = Post.objects.create(author=author, **validated_data)
            return post
        else:
            raise serializers.ValidationError("지자체 관리자만 글을 쓸 수 있는 게시판이예요🦁")
