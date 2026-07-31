from django.shortcuts import render
from apps.users.serializers import RegisterSerializer, AddressSerializer
from apps.users.models import Address
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


''' template views '''
def login(request):
    return render(request, "users/login.html")


def register(request):
    return render(request, "users/register.html")


''' API viewsets '''
class RegisterViewSet(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class AddressView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # para evitar que um outro usuário salve um endereço que não é dele. essa função faz com que o endereço cadastrado seja sempre do usuário cadastrando ele.