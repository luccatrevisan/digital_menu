from django.shortcuts import render

from apps.users.serializers import RegisterSerializer

from rest_framework import generics
from rest_framework.permissions import AllowAny


''' template views '''
def login(request):
    return render(request, "users/login.html")


def register(request):
    return render(request, "users/register.html")


''' API viewsets '''
class RegisterViewSet(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer