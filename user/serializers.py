from rest_framework import serializers
from .models import User

        
class UserSerializer(serializers.ModelSerializer):
    liked_posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = "__all__"