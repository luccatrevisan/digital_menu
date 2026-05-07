from django.urls import path
from apps.users.views import login, register
from apps.users.views import RegisterViewSet


urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("api/register/", RegisterViewSet.as_view(), name="api-register"),
]