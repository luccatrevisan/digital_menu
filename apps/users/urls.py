from django.urls import path
from apps.users.views import login, register
from apps.users.views import RegisterViewSet, AddressView


urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("api/register/", RegisterViewSet.as_view(), name="api-register"),
    path("api/address/", AddressView.as_view(), name="api-address")
]