from rest_framework import serializers
from apps.menu.models import MenuItem, Stock


class OrderItemInputSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemInputSerializer(many=True)
    
    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError(
                detail={
                    "message" : "The cart cannot be empty.",
                    "code" : "empty_cart"
                }
            )

        for item in items:
            try:
                menu_item = MenuItem.objects.get(pk=item["menu_item_id"])

                if not menu_item.is_available:
                    raise serializers.ValidationError(
                        detail={
                            "message" : f"{menu_item.name} is not available.",
                            "menu_item" : f"{menu_item.name}",
                            "code" : "item_unavailable"
                        }
                    )
                
            except MenuItem.DoesNotExist:
                raise serializers.ValidationError(
                    detail={
                        "message" : f"Menu item {item['menu_item_id']} does not exist.",
                        "code" : "item_does_not_exist"
                    }
                )

            try:
                stock = Stock.objects.get(menu_item=menu_item)
            
                if stock.quantity < item["quantity"]:
                    raise serializers.ValidationError(
                        detail={
                            "message" : f"Only {stock.quantity} units available.",
                            "menu_item" : f"{menu_item.name}",
                            "remaining" : f"{stock.quantity}",
                            "code" : "stock_unavailable"
                        }
                    )
            
            except Stock.DoesNotExist:
                pass

        return items