# from django.contrib.auth.password_validation import validate_password
# from rest_framework import serializers
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate
# from user.models import User


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         validators=[validate_password]
#     )
#     password2 = serializers.CharField(write_only=True, required=True)
    
#     # birthday = serializers.DateField(required=True)
#     # address = serializers.CharField(required=True)
#     # nickname = serializers.CharField(required=True)
    
#     class Meta:
#         model = User.username.field.related_model
#         fields = ('username', 'password', 'password2') #"birthday", "address", "nickname"
        
#     def validate(self, data):
#         if data['password'] != data['password2']:
#             raise serializers.ValidationError(
#                 {"password": "비밀번호가 일치하지 않습니다!"}
#             )
        
#         return data
    
#     def create(self, validated_data):
#         user = User.username.field.related_model.objects.create_user(
#             username=validated_data['username'],
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         token, created = Token.objects.get_or_create(user=user)
#         return user


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True, write_only=True)
    
#     def validate(self, data):
#         user = authenticate(**data)
#         if user:
#             token = Token.objects.get(user=user)
#             return token
#         raise serializers.ValidationError(
#             {"error": "로그인 실패ㅠㅠ 아이디 또는 비밀번호가 틀립니다."}
#         )


from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)  # email 필드 추가

    class Meta:
        model = User
        # fields = ('username', 'password', 'password2')
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다!"}
            )
        return data

    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #         username=validated_data['username'],
    #         password=validated_data['password']
    #     )
    #     user.save()
    #     return user
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],  # 추가: email 필드를 제공
            password=validated_data['password']
        )
        token, created = Token.objects.get_or_create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return token
        raise serializers.ValidationError(
            {"error": "로그인 실패ㅠㅠ 아이디 또는 비밀번호가 틀립니다."}
        )