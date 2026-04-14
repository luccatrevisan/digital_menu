from django.shortcuts import render

from rest_framework import viewsets, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from apps.menu.serializers import CategorySerializer, MenuItemSerializer, StockSerializer, MenuItemWithStockSerializer, MenuItemByCategorySerializer, ComplementSerializer, ComplementGroupSerializer, ComplementByGroupSerializer

from apps.menu.models import Category, MenuItem, Stock, Complement, ComplementGroup

from apps.menu.permissions import IsAdminOrReadOnly


''' views '''
def index(request):
    return render(request, "menu/index.html")


''' viewsets '''
class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class MenuItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()


class StockViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    serializer_class = StockSerializer
    queryset = Stock.objects.all()


class ComplementViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    serializer_class = ComplementSerializer
    queryset = Complement.objects.all()


class ComplementGroupViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    serializer_class = ComplementGroupSerializer
    queryset = ComplementGroup.objects.all()


''' generics '''
class ComplementByGroupViewSet(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ComplementByGroupSerializer
    queryset = ComplementGroup.objects.prefetch_related("complements").all()


class MenuItemWithStockViewSet(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = MenuItemWithStockSerializer
    queryset = MenuItem.objects.prefetch_related("complementgroup_set").all().select_related("stock")


class MenuItemByCategoryViewSet(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = MenuItemByCategorySerializer
    queryset = Category.objects.prefetch_related("menuitem_set__complementgroup_set__complements").all()