from django.db import transaction
from django.core.exceptions import ValidationError
from apps.orders.models import OrderItem
from apps.menu.models import Stock


@transaction.atomic
def add_item_to_cart(order, menu_item, quantity):
    if order.status != order.Status.PENDING:
        raise ValidationError(
            "Items can only be added to pending orders."
        )

    if quantity <= 0:
        raise ValidationError(
            "Quantity must be greater than zero."
        )

    try:
        stock = Stock.objects.select_for_update().get(
            menu_item=menu_item
        )

    except Stock.DoesNotExist:
        raise ValidationError(
            f"Stock for '{menu_item.name}' does not exist."
        )

    existing_item = OrderItem.objects.filter(
        order=order,
        menu_item=menu_item
    ).first()

    current_quantity = existing_item.quantity if existing_item else 0
    new_quantity = current_quantity + quantity

    if (
        stock.quantity is not None
        and new_quantity > stock.quantity
    ):
        raise ValidationError(
            f"Insufficient stock for '{menu_item.name}'. "
            f"Available: {stock.quantity}"
        )

    if existing_item:
        existing_item.quantity = new_quantity
        existing_item.save()

        return existing_item

    return OrderItem.objects.create(
        order=order,
        menu_item=menu_item,
        quantity=quantity
    )