from apps.orders.models import Order
from django.core.exceptions import ValidationError
from decimal import Decimal
import pytest

''' valid transitions '''
def test_confirm_order(order, order_item):
    order.confirm_order()
    order.refresh_from_db()
    assert order.status == Order.Status.CONFIRMED


def test_start_preparing(order, order_item):
    order.status = Order.Status.CONFIRMED
    order.save()

    order.start_preparing()
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
        order.start_preparing()


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