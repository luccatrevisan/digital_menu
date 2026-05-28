from apps.orders.models import Order
from django.core.exceptions import ValidationError
import pytest

def test_confirm_order_populates_delivery_fields(order, order_item, address):
    order.confirm_order()
    order.refresh_from_db()

    assert order.delivery_cep == address.cep
    assert order.delivery_street == address.street
    assert order.delivery_number == address.number
    assert order.delivery_complement == address.complement
    assert order.delivery_neighborhood == address.neighborhood
    assert order.delivery_city == address.city
    assert order.delivery_state == address.state
    assert order.delivery_label == address.label


def test_delivery_snapshot_remains_after_address_update(order, order_item, address):
    order.address = address
    order.save()
    order.confirm_order()

    old_street = order.delivery_street
    old_city = order.delivery_city
    old_cep = order.delivery_cep


    address.street = "New Street"
    address.city = "New City"
    address.cep = "37000-000"
    address.save()

    order.refresh_from_db()

    assert order.delivery_street == old_street


def test_delivery_order_requires_address(order, order_item):
    order.delivery_type = Order.DeliveryType.DELIVERY
    order.address = None
    order.save()

    with pytest.raises(ValidationError):
        order.confirm_order()


def test_pickup_order_does_not_require_address(order, order_item):
    order.delivery_type = Order.DeliveryType.PICKUP
    order.address = None
    order.save()

    order.confirm_order()
    order.refresh_from_db()

    assert order.status == Order.Status.CONFIRMED


def test_pickup_order_keeps_delivery_fields_empty(order, order_item):
    order.delivery_type = Order.DeliveryType.PICKUP
    order.address = None
    order.save()

    order.confirm_order()
    order.refresh_from_db()

    assert order.delivery_street is None
    assert order.delivery_city is None
    assert order.delivery_cep is None