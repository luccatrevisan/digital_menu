from django.urls import path
from apps.users.views import login, register
from apps.orders.views import OrdersView


urlpatterns = [
    path("api/orders/", OrdersView.as_view(), name="api-orders"),
]

