from apps.orders.models import Order

def get_or_create_pending_order(user):
    order = Order.objects.get_or_create(
        user=user,
        status=Order.Status.PENDING
    )

    return order