from django.urls import path, include
from apps.menu.views import index, CategoryViewSet, MenuItemViewSet, StockViewSet, MenuItemWithStockViewSet, MenuItemByCategoryViewSet, ComplementViewSet, ComplementGroupViewSet, ComplementByGroupViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('menuitems', MenuItemViewSet)
router.register('stock', StockViewSet)
router.register('complements', ComplementViewSet)
router.register('complement-groups', ComplementGroupViewSet)


urlpatterns = [
    path("", index),
    path("api/", include(router.urls)),
    path("api/item-by-category/", MenuItemByCategoryViewSet.as_view(), name="item-by-category"),
    path("api/item-with-stock/", MenuItemWithStockViewSet.as_view(), name="item-with-stock"),
    path("api/complement-by-group", ComplementByGroupViewSet.as_view(), name="complement-by-group"),
]