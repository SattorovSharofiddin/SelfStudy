from django.shortcuts import render
from rest_framework import generics, permissions

from users.models import User, Instructor
from users.serializers import RegisterSerializer, UserSerializer


# Register API
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        if user.role == 'instructor':
            Instructor.objects.create(user=user)
