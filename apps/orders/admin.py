from django.contrib import admin
from apps.orders.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ["status", "total_price", "created_at"]
    search_fields = ["status", "total_price", "created_at"]
    list_filter = ["status", "total_price", "created_at"]
    ordering = ["created_at"]

admin.site.register(Order)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["menu_item", "quantity", "subtotal"]
    list_filter = ["menu_item", "quantity", "subtotal"]
    ordering = ["id"]

admin.site.register(OrderItem)