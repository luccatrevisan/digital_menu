from apps.menu.models import MenuItem, Stock, Category, Complement, ComplementGroup
from decimal import Decimal
from django.core.exceptions import ValidationError
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


'''tests the stock quantity for negative values'''
def test_negative_quantity_stock(stock):
    with pytest.raises(ValidationError):
        stock.quantity = -4
        stock.full_clean()    


'''complement and complementgroup'''
@pytest.fixture
def complement(db):
    return Complement.objects.create(name="Ouro 1")


@pytest.fixture
def complement_group(db, menu_item, complement):
    complement_group = ComplementGroup.objects.create(name="Ourinhos", menu_item=menu_item, min_quantity=3, max_quantity=3)

    complement_group.complements.add(complement)
    complement_group.save()

    return complement_group


def test_min_quantity_higher(complement_group):
    with pytest.raises(ValidationError):
        complement_group.min_quantity = 5
        complement_group.save()