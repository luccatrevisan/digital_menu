from django.db import transaction
from django.core.exceptions import ValidationError
from apps.orders.models import Order, OrderItem
from apps.menu.models import MenuItem, Stock


def create_order(items_data): 
    try:
        with transaction.atomic():
            order = Order.objects.create()

            for item_data in items_data:
                menu_item_id = item_data.get("menu_item_id")
                quantity = item_data.get("quantity")

                # validate menu item existence
                try:
                    menu_item = MenuItem.objects.get(id=menu_item_id)

                except MenuItem.DoesNotExist:
                    raise ValidationError(
                        f"Menu item with id {menu_item_id} does not exist."
                    )

                # validate stock existence
                try:
                    stock = Stock.objects.select_for_update().get(menu_item=menu_item)

                except Stock.DoesNotExist:
                    raise ValidationError(
                        f"Stock for '{menu_item.name}' does not exist."
                    )

                # validate stock quantity
                if stock.quantity is not None and quantity > stock.quantity:
                    raise ValidationError(
                        f"Insufficient stock for '{menu_item.name}'. "
                        f"Available: {stock.quantity}"
                    )

                # create order item
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity
                )

                # decreases stock
                if stock.quantity is not None:
                    stock.quantity -= quantity
                    stock.save(update_fields=["quantity"])

            # update total order price
            order.update_total_price()

            return order

    except ValidationError as e:
        raise ValidationError(
            {"order_error": e.message}
        )

    except Exception as e:
        raise ValidationError(
            f"Unexpected error while creating order: {str(e)}"
    )