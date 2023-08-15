from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from user.models import User, Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다!"}
            )
        return data

    def create(self, validated_data):
        user = Profile.user.field.related_model.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return token
        raise serializers.ValidationError(
            {"error": "로그인 실패ㅠㅠ 이메일 또는 비밀번호가 틀립니다."}
        )