from django.contrib import admin
from menu.models import Category, MenuItem, Stock


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]
    search_fields = ["id", "name"]
    list_filter = ["id", "name"]

admin.site.register(Category, CategoryAdmin)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "name", "category", "old_price", "price", "is_available"]
    list_display_links = ["id", "name"]
    search_fields = ["id", "name", "category"]
    list_filter = ["id", "name", "category", "price"]
    ordering = ["id"]

admin.site.register(MenuItem, MenuItemAdmin)


class StockAdmin(admin.ModelAdmin):
    list_display = ["menu_item", "quantity"]
    list_filter = ["quantity"]

admin.site.register(Stock, StockAdmin)