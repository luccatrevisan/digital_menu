from django.db.models.signals import (post_save, post_delete)
from django.dispatch import receiver


@receiver(post_save, sender="menu.Stock", dispatch_uid="menu_stock_post_save_availability")
def menu_item_availability(sender, instance, **kwargs):
    if instance.quantity is None or instance.quantity > 0:
        instance.menu_item.is_available = True
    else:
        instance.menu_item.is_available = False
    instance.menu_item.save(update_fields=["is_available"])


@receiver(post_delete, sender="menu.Stock", dispatch_uid="menu_stock_post_delete_availability")
def handle_deleted_stock(sender, instance, **kwargs):
    instance.menu_item.is_available = True
    instance.menu_item.save(update_fields=["is_available"])