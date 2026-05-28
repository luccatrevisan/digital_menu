from apps.orders.models import Order, OrderItem
from apps.users.models import CustomUser, Address
from apps.menu.models import Category, MenuItem
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