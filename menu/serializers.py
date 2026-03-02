from rest_framework import serializers
from menu.models import Category, MenuItem, Stock, Complement, ComplementGroup


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["menu_item", "quantity"]


class ComplementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complement
        fields = "__all__"


class ComplementGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplementGroup
        fields = "__all__"


''' nested serializers '''
class ComplementByGroupSerializer(serializers.ModelSerializer):
    complements = ComplementSerializer(many=True, read_only=True)

    class Meta:
        model = ComplementGroup
        fields = ["name", "min_quantity", "max_quantity", "complements"]


class MenuItemWithStockSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    complementgroup = ComplementByGroupSerializer(many=True, read_only=True, source="complementgroup_set")

    class Meta:
        model = MenuItem
        fields = ["id", "name", "description", "price", "old_price", "image", "stock", "is_available", "complementgroup"]


class MenuItemByCategorySerializer(serializers.ModelSerializer):
    menu_items = MenuItemWithStockSerializer(many=True, read_only=True, source="menuitem_set")

    class Meta:
        model = Category
        fields = ["id", "name", "menu_items"]