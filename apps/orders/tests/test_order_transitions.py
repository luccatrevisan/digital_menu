from apps.orders.models import Order, OrderItem
from apps.users.models import CustomUser, Address
from apps.menu.models import Category, MenuItem
from django.core.exceptions import ValidationError
from decimal import Decimal
import pytest



''' category '''
@pytest.fixture
def category(db):
    return Category.objects.create(name="Pedacinho do Céu")


''' menu item '''
@pytest.fixture
def menu_item(db, category):
    return MenuItem.objects.create(
        name="Cookie de Ouro", 
        category=category, 
        description="Muito gostoso", 
        price=Decimal("24.99"), 
        image="docs/img/roadmap.png"
    )


''' user '''
@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
        username="lucca",
        email="lucca@test.com",
        password="123456",
        phone_number="21999999999"
    )


''' address '''
@pytest.fixture
def address(db, user):
    return Address.objects.create(
        user=user,
        cep="20000-000",
        street="Rua dos Cookies",
        number="123",
        neighborhood="Centro",
        city="Niteroi",
        state="RJ",
        label="CASA"
    )


''' order item '''
@pytest.fixture
def order_item(db, order, menu_item):
    return OrderItem.objects.create(
        order=order,
        menu_item=menu_item,
        quantity=2
    )


''' order '''
@pytest.fixture
def order(db, user, address):
    return Order.objects.create(
        user=user,
        address=address
    )


''' valid transitions '''
def test_confirm_order(order, order_item):
    order.confirm_order()
    order.refresh_from_db()
    assert order.status == Order.Status.CONFIRMED


def test_start_order(order, order_item):
    order.status = Order.Status.CONFIRMED
    order.save()

    order.start_order()
    order.refresh_from_db()

    assert order.status == Order.Status.PREPARING


def test_mark_ready(order, order_item):
    order.status = Order.Status.PREPARING
    order.save()

    order.mark_ready()
    order.refresh_from_db()

    assert order.status == Order.Status.READY


def test_start_delivery(order, order_item):
    order.status = Order.Status.READY
    order.save()

    order.start_delivery()
    order.refresh_from_db()

    assert order.status == Order.Status.DELIVERING


def test_complete_order(order, order_item):
    order.status = Order.Status.DELIVERING
    order.save()

    order.complete_order()
    order.refresh_from_db()

    assert order.status == Order.Status.COMPLETED


def test_cancel_order(order):
    order.cancel_order()
    order.refresh_from_db()

    assert order.status == Order.Status.CANCELLED


''' invalid transitions '''
def test_confirm_non_pending_order(order):
    order.status = Order.Status.COMPLETED
    order.save()

    with pytest.raises(ValidationError):
        order.confirm_order()


def test_start_non_confirmed_order(order):
    with pytest.raises(ValidationError):
        order.start_order()


def test_mark_ready_non_preparing_order(order):
    with pytest.raises(ValidationError):
        order.mark_ready()


def test_start_delivery_non_ready_order(order):
    with pytest.raises(ValidationError):
        order.start_delivery()


def test_complete_non_delivering_order(order):
    with pytest.raises(ValidationError):
        order.complete_order()


def test_cancel_completed_order(order):
    order.status = Order.Status.COMPLETED
    order.save()

    with pytest.raises(ValidationError):
        order.cancel_order()


''' business rules '''
def test_confirm_order_without_minimum_price(order, order_item):
    order.total_price = Decimal("10.00")
    order.save()

    with pytest.raises(ValidationError):
        order.confirm_order()