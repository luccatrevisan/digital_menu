from django.core.exceptions import ValidationError
from apps.orders.models import OrderItem


def remove_item_from_cart(order, menu_item):
    if order.status != order.Status.PENDING:
        raise ValidationError(
            "Items can only be removed from pending orders."
        )

    try:
        order_item = OrderItem.objects.get(
            order=order,
            menu_item=menu_item
        )

    except OrderItem.DoesNotExist:
        raise ValidationError(
            "This item is not in the cart."
        )

    order_item.delete()