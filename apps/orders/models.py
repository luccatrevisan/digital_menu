from decimal import Decimal
from django.db import models
from apps.menu.models import MenuItem, Complement, ComplementGroup
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from apps.users.models import CustomUser, Address 


class Order(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=False, blank=False)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="orders", null=True, blank=True)

    def update_total_price(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_price = total
        self.save(update_fields=["total_price"])

    def validate_minimum_price(self):
        if self.total_price < 30:
            raise ValidationError("The total price should be R$30,00 or more.")

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2) 


    def clean(self):
        if self.unit_price < Decimal("0"):
            raise ValidationError("Unit price cannot be negative.")


    def save(self, *args, **kwargs):
        self.unit_price = self.menu_item.price
        self.subtotal = self.unit_price * self.quantity

        self.full_clean()
        super().save(*args, **kwargs)

        self.order.update_total_price()

    
    def delete(self, *args, **kwargs):
        order = self.order

        super().delete(*args, **kwargs)
        
        order.update_total_price()


    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
    

class OrderItemComplement(models.Model):
    ...