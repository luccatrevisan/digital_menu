from django.shortcuts import render
from rest_framework import viewsets, generics
from menu.serializers import CategorySerializer, MenuItemSerializer, StockSerializer, MenuItemByCategorySerializer
from menu.models import Category, MenuItem, Stock


''' views '''
def index(request):
    return render(request, "menu/index.html")


''' viewsets '''
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()


class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


class MenuItemByCategoryViewSet(generics.ListAPIView):
    serializer_class = MenuItemByCategorySerializer
    queryset = Category.objects.prefetch_related("menuitem_set").all()