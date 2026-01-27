from django.urls import path
from menu.views import home

urlpatterns = [
    path("", home),
]