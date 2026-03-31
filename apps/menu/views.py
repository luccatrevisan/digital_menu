from django.shortcuts import render
from rest_framework import viewsets, generics
from apps.menu.serializers import CategorySerializer, MenuItemSerializer, StockSerializer, MenuItemWithStockSerializer, MenuItemByCategorySerializer, ComplementSerializer, ComplementGroupSerializer, ComplementByGroupSerializer
from apps.menu.models import Category, MenuItem, Stock, Complement, ComplementGroup


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


class ComplementViewSet(viewsets.ModelViewSet):
    serializer_class = ComplementSerializer
    queryset = Complement.objects.all()


class ComplementGroupViewSet(viewsets.ModelViewSet):
    serializer_class = ComplementGroupSerializer
    queryset = ComplementGroup.objects.all()


''' generics '''
class ComplementByGroupViewSet(generics.ListAPIView):
    serializer_class = ComplementByGroupSerializer
    queryset = ComplementGroup.objects.prefetch_related("complements").all()


class MenuItemWithStockViewSet(generics.ListAPIView):
    serializer_class = MenuItemWithStockSerializer
    queryset = MenuItem.objects.prefetch_related("complementgroup_set").all().select_related("stock")


class MenuItemByCategoryViewSet(generics.ListAPIView):
    serializer_class = MenuItemByCategorySerializer
    queryset = Category.objects.prefetch_related("menuitem_set__complementgroup_set__complements").all()