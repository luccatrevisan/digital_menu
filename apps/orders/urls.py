from django.urls import path
from apps.orders.views import OrdersView, order_success


urlpatterns = [
    path("api/orders/", OrdersView.as_view(), name="api-orders"),
    path("orders/success/", order_success, name="order-success"),
]

