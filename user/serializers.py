from rest_framework import serializers
from .models import Profile, EditorProfile

        
class ProfileSerializer(serializers.ModelSerializer):
    liked_posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Profile
        fields = ['user', 'birthday', 'nickname', 'address', 'liked_posts']
        

class EditorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditorProfile
        fields = ['name', 'address']

    def create(self, validated_data):
        user = self.context['request'].user

        if not user.is_authenticated:
            raise serializers.ValidationError("로그인한 사용자만 프로필을 생성할 수 있습니다.")

        validated_data['user'] = user
        editor_profile = EditorProfile.objects.create(**validated_data)
        return editor_profile