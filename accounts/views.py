# from django.shortcuts import render
# # from django.contrib.auth.models import User
# from rest_framework.generics import CreateAPIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import generics
# from .serializers import RegisterSerializer, LoginSerializer
# from user.models import User 
# from rest_framework.permissions import AllowAny

# # class RegisterView(CreateAPIView):
# #     queryset = User.objects.all()
# #     serializer_class = RegisterSerializer
# class RegisterView(CreateAPIView):
#     serializer_class = RegisterSerializer
#     permission_classes = [AllowAny]
    
    
# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     # permission_classes = [AllowAny]
    
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         token = serializer.validated_data
#         return Response({"token":token.key}, status=status.HTTP_200_OK)

from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import RegisterSerializer, LoginSerializer
from user.models import User 
from rest_framework.permissions import AllowAny


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({"token":token.key}, status=status.HTTP_200_OK)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)