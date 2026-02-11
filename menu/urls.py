from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from menu.views import index, CategoryViewSet, MenuItemViewSet, StockViewSet, MenuItemByCategoryViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('menuitems', MenuItemViewSet)
router.register('stock', StockViewSet)

urlpatterns = [
    path("", index),
    path("api/", include(router.urls)),
    path("api/item-by-category/", MenuItemByCategoryViewSet.as_view(), name="item-by-category")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)