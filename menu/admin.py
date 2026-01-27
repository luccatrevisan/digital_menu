from django.contrib import admin
from menu.models import Category, MenuItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]
    search_fields = ["id", "name"]
    list_filter = ["id", "name"]

admin.site.register(Category, CategoryAdmin)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "name", "category", "price"]
    search_fields = ["id", "name", "category"]
    list_filter = ["id", "name", "category", "price"]

admin.site.register(MenuItem, MenuItemAdmin)