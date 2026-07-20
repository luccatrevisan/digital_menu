from django.db import transaction
from django.core.exceptions import ValidationError
from apps.orders.models import Order, OrderItem
from apps.menu.models import MenuItem, Stock

'''
    payload = {
        "items": [
            {
                "menu_item_id": 3,
                "quantity": 2
            },
            {
                "menu_item_id" : 4,
                "quantity" : 1
            }
        ]
    }
'''

def create_order(user, items_data):
    with transaction.atomic():
        order = Order.objects.create(
            user = user
        )

        for item in items_data:
            menu_item_id = item.get("menu_item_id")
            quantity = item.get("quantity")

            menu_item = MenuItem.objects.get(pk=menu_item_id)
            stock = Stock.objects.select_for_update().get(menu_item=menu_item)
        
            # decreases stock
            if stock.quantity is not None:
                stock.quantity -= quantity
                stock.save(update_fields=["quantity"])

            
            # create order item
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity
            )

        # update total order price
        order.update_total_price()
        order.validate_minimum_price()


        return order