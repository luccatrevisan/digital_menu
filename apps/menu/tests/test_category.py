import pytest
from apps.menu.models import Category


@pytest.fixture
def category(db):
    return Category.objects.create(name="Pedacinho do Céu")


def test_category(category):
    assert category.name == "Pedacinho do Céu"