import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.orders.models import Order, OrderItem
from apps.menu.models import MenuItem


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
    )

    return client


@pytest.mark.django_db
def test_create_order_success(authenticated_client, menu_item):
    payload = {
        "items": [
            {
                "menu_item_id": menu_item.id,
                "quantity": 2
            }
        ]
    }

    response = authenticated_client.post(
        "/api/orders/",
        payload,
        format="json"
    )

    assert response.status_code == 201
    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 1


@pytest.mark.django_db
def test_create_order_requires_authentication(menu_item):
    client = APIClient()

    payload = {
        "items": [
            {
                "menu_item_id": menu_item.id,
                "quantity": 2
            }
        ]
    }

    response = client.post(
        "/api/orders/",
        payload,
        format="json"
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_create_order_with_empty_cart(
    authenticated_client
):
    payload = {
        "items": []
    }

    response = authenticated_client.post(
        "/api/orders/",
        payload,
        format="json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_order_with_invalid_menu_item(
    authenticated_client
):
    payload = {
        "items": [
            {
                "menu_item_id": 999,
                "quantity": 1
            }
        ]
    }

    response = authenticated_client.post(
        "/api/orders/",
        payload,
        format="json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_order_quantity_exceeds_stock(authenticated_client, menu_item, stock):
    payload = {
        "items": [
            {
                "menu_item_id": menu_item.id,
                "quantity": 999
            }
        ]
    }

    response = authenticated_client.post(
        "/api/orders/",
        payload,
        format="json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_order_with_multiple_items(authenticated_client, menu_item, category):
    second_item = MenuItem.objects.create(
        name="Cookie de Chocolate",
        category=category,
        description="Muito gostoso também",
        price=10.00,
        image="docs/img/test.png"
    )

    payload = {
        "items": [
            {
                "menu_item_id": menu_item.id,
                "quantity": 2
            },
            {
                "menu_item_id": second_item.id,
                "quantity": 3
            }
        ]
    }

    response = authenticated_client.post(
        "/api/orders/",
        payload,
        format="json"
    )

    assert response.status_code == 201
    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 2

    order = Order.objects.first()
    assert order.items.count() == 2
    assert order.total_price > 0
    
    expected_total = (menu_item.price * 2 + second_item.price * 3)
    assert order.total_price == expected_total

    order_items = order.items.all()
    assert {item.quantity for item in order_items} == {2, 3}