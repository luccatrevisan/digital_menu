from django.db import transaction
from django.core.exceptions import ValidationError
from apps.orders.models import Order, OrderItem
from apps.menu.models import MenuItem, Stock


def create_order(user, items_data): 
    with transaction.atomic():
        order = Order.objects.create(
            user = user
        )

        for item in items_data:
            menu_item_id = item.get("menu_item_id")
            quantity = item.get("quantity")

            # validate menu item existence
            try:
                menu_item = MenuItem.objects.get(id=menu_item_id)

            except MenuItem.DoesNotExist:
                raise ValidationError(
                    f"Menu item with id {menu_item_id} does not exist."
                )
            
            if menu_item.is_available is False:
                raise ValidationError("This product is not available")
            
            

            # validate stock quantity
            try:
                stock = Stock.objects.select_for_update().get(menu_item=menu_item)

                if stock.quantity is not None and quantity > stock.quantity:
                    raise ValidationError(
                        f"Insufficient stock for '{menu_item.name}'. "
                        f"Available: {stock.quantity}"
                    )
            
                # decreases stock
                if stock.quantity is not None:
                    stock.quantity -= quantity
                    stock.save(update_fields=["quantity"])

            except Stock.DoesNotExist:
                pass

            
            # create order item
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity
            )

        # update total order price
        order.update_total_price()
        order.confirm_order()

        return order