import pytest
import threading
from django.core.exceptions import ValidationError
from apps.orders.models import Order, OrderItem
from apps.orders.services.create_order import create_order
from apps.menu.models import MenuItem


@pytest.mark.django_db
def test_create_order_service_creates_order(user, menu_item):
    order = create_order(
        user=user,
        items_data=[
            {
                "menu_item_id": menu_item.id,
                "quantity": 2,
            }
        ]
    )

    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 1
    assert order.user == user


@pytest.mark.django_db
def test_create_order_service_creates_multiple_order_items(
    user,
    menu_item,
    category,
):
    second_item = MenuItem.objects.create(
        name="Cookie Chocolate",
        category=category,
        description="...",
        price=10,
        image="docs/img/test.png"
    )

    order = create_order(
        user=user,
        items_data=[
            {
                "menu_item_id": menu_item.id,
                "quantity": 2,
            },
            {
                "menu_item_id": second_item.id,
                "quantity": 3,
            }
        ]
    )

    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 2
    assert order.items.count() == 2


@pytest.mark.django_db
def test_create_order_service_decreases_stock(
    user,
    menu_item,
    stock,
):
    initial_quantity = stock.quantity

    create_order(
        user=user,
        items_data=[
            {
                "menu_item_id": menu_item.id,
                "quantity": 2,
            }
        ]
    )

    stock.refresh_from_db()

    assert stock.quantity == initial_quantity - 2


@pytest.mark.django_db
def test_create_order_service_does_not_change_unlimited_stock(
    user,
    menu_item,
):
    order = create_order(
    user=user,
    items_data=[
            {
                "menu_item_id": menu_item.id,
                "quantity": 2,
            }
        ]
    )

    assert Order.objects.count() == 1
    assert order.items.count() == 1


@pytest.mark.django_db
def test_create_order_service_rejects_order_below_minimum_price(
    user,
    menu_item,
):
    with pytest.raises(ValidationError):

        create_order(
            user=user,
            items_data=[
                {
                    "menu_item_id": menu_item.id,
                    "quantity": 1,
                }
            ]
        )


@pytest.mark.django_db
def test_create_order_service_rolls_back_transaction_when_validation_fails(
    user,
    menu_item,
    stock,
):
    initial_quantity = stock.quantity

    with pytest.raises(ValidationError):
        create_order(
            user=user,
            items_data=[
                {
                    "menu_item_id": menu_item.id,
                    "quantity": 1,
                }
            ]
        )

    stock.refresh_from_db()

    assert Order.objects.count() == 0
    assert OrderItem.objects.count() == 0
    assert stock.quantity == initial_quantity


@pytest.mark.django_db
def test_create_order_service_updates_total_price(
    user,
    menu_item,
):
    order = create_order(
        user=user,
        items_data=[
            {
                "menu_item_id": menu_item.id,
                "quantity": 2,
            }
        ]
    )

    assert order.total_price == menu_item.price * 2


@pytest.mark.django_db
def test_create_order_service_saves_price_snapshot(
    user,
    menu_item,
):
    original_price = menu_item.price

    order = create_order(
        user=user,
        items_data=[
            {
                "menu_item_id": menu_item.id,
                "quantity": 2,
            }
        ]
    )

    menu_item.price = 99
    menu_item.save()

    order_item = order.items.first()

    assert order_item.unit_price == original_price


@pytest.mark.django_db
def test_two_sequential_orders_decrement_stock_cumulatively(menu_item, stock, user):
    stock.quantity = 10
    stock.save()

    create_order(user, [{"menu_item_id": menu_item.id, "quantity": 2}])
    create_order(user, [{"menu_item_id": menu_item.id, "quantity": 3}])

    stock.refresh_from_db()
    assert stock.quantity == 5


@pytest.mark.django_db(transaction=True)
def test_concurrent_orders_do_not_oversell_stock(menu_item, stock, user):
    stock.quantity = 1
    stock.save()

    barrier = threading.Barrier(2)

    def place_order():
        barrier.wait()
        from django.db import connection

        try:
            create_order(user, [{"menu_item_id": menu_item.id, "quantity": 1}])
        finally:
            connection.close()

    threads = [threading.Thread(target=place_order) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    stock.refresh_from_db()
    assert stock.quantity >= 0, "Estoque ficou negativo — overselling ocorreu."