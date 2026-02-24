from django.contrib import admin
from menu.models import Category, MenuItem, Stock, Complement, ComplementGroup


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


class ComplementAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]
    ordering = ["id"]

admin.site.register(Complement, ComplementAdmin)


class ComplementGroupAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "menu_item", "min_quantity", "max_quantity"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "menu_item"]
    ordering = ["id"]

admin.site.register(ComplementGroup, ComplementGroupAdmin)