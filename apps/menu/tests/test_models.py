from apps.menu.models import MenuItem, Stock, Category, Complement, ComplementGroup
from decimal import Decimal
import pytest


'''category'''
@pytest.fixture
def category(db):
    return Category.objects.create(name="Pedacinho do Céu")


def test_category(category):
    assert category.name == "Pedacinho do Céu"


'''menu item'''
@pytest.fixture
def menu_item(db, category):
    return MenuItem.objects.create(name="Cookie de Ouro", category=category, description="Muito gostoso", price=Decimal("1.99"), image="docs/img/roadmap.png")


def test_menu_item(menu_item):
    assert menu_item.name == "Cookie de Ouro"


'''stock'''
@pytest.fixture
def stock(db, menu_item):
    return Stock.objects.create(menu_item=menu_item)


'''tests the business logic between menuitem and the creation of its stock'''
def test_availability_when_none(menu_item, stock):
    stock.quantity = None
    stock.save()

    menu_item = MenuItem.objects.get(id=menu_item.id)

    assert menu_item.is_available == True


def test_availability_when_positive(menu_item, stock):
    stock.quantity = 3
    stock.save()

    menu_item = MenuItem.objects.get(id=menu_item.id)

    assert menu_item.is_available is True


def test_availability_when_zero(menu_item, stock):
    stock.quantity = 0
    stock.save()

    menu_item = MenuItem.objects.get(id=menu_item.id)

    assert menu_item.is_available == False


def test_availability_update(menu_item, stock):
    stock.quantity = 0
    stock.save()

    menu_item = MenuItem.objects.get(id=menu_item.id)
    
    assert menu_item.is_available == False


    stock.quantity = 5
    stock.save()

    menu_item = MenuItem.objects.get(id=menu_item.id)

    assert menu_item.is_available == True


'''tests the deletion handling business logic between item and its stock'''
def test_deletion_handling(menu_item, stock):
    stock.delete()
    menu_item.save()

    menu_item = MenuItem.objects.get(id=menu_item.id)

    assert menu_item.is_available == True


'''complement and complementgroup'''
