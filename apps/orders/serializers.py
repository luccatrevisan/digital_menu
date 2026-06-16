from rest_framework import serializers
from apps.menu.models import MenuItem, Stock


class OrderItemInputSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemInputSerializer(many=True)
    
    def validate_items(self, items):
        for item in items:
            try:
                menu_item = MenuItem.objects.get(pk=item["menu_item_id"])

                if not menu_item.is_available:
                    raise serializers.ValidationError(f"{menu_item.name} is not available.")
                
            except MenuItem.DoesNotExist:
                raise serializers.ValidationError(f"Menu item {item['menu_item_id']} does not exist.")

            try:
                stock = Stock.objects.get(menu_item=menu_item)
            
                if stock.quantity < item["quantity"]:
                    raise serializers.ValidationError(f"Only {stock.quantity} units available.")
            
            except Stock.DoesNotExist:
                pass

        if not items:
            raise serializers.ValidationError("O carrinho não pode ficar vazio.")

        return items