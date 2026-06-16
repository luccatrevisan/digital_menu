from apps.orders.models import Order
from django.core.exceptions import ValidationError
from apps.orders.serializers import OrderCreateSerializer, OrderItemInputSerializer
import pytest

@pytest.mark.django_db
def test_if_menu_item_does_not_exist(menu_item):
    payload = {
        "items": [
            {
                "menu_item_id": 999,
                "quantity": 1,
            }
        ]
    }

    serializer = OrderCreateSerializer(data=payload)

    assert not serializer.is_valid()
    assert "does not exist" in str(serializer.errors)


def test_if_menu_item_is_unavailable(menu_item):
    menu_item.is_available = False
    menu_item.save()

    payload = {
        "items": [
            {
                "menu_item_id": menu_item.id,
                "quantity": 1,
            }
        ]
    }

    serializer = OrderCreateSerializer(data=payload)

    assert not serializer.is_valid()
    assert "not available" in str(serializer.errors)


def test_if_requested_quantity_exceeds_stock(menu_item, stock):
    payload = {
        "items": [
            {
                "menu_item_id": menu_item.id,
                "quantity": 10,
            }
        ]
    }

    serializer = OrderCreateSerializer(data=payload)

    assert not serializer.is_valid()
    assert "units available" in str(serializer.errors)


def test_allow_item_without_stock(menu_item):
    payload = {
        "items": [
            {
                "menu_item_id": menu_item.id,
                "quantity": 999,
            }
        ]
    }

    serializer = OrderCreateSerializer(data=payload)

    assert serializer.is_valid()


def test_valid_payload(menu_item, stock):
    payload = {
        "items": [
            {
                "menu_item_id": menu_item.id,
                "quantity": 2,
            }
        ]
    }

    serializer = OrderCreateSerializer(data=payload)

    assert serializer.is_valid()