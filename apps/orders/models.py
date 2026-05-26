from decimal import Decimal
from django.db import models
from apps.menu.models import MenuItem, Complement, ComplementGroup
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from apps.users.models import CustomUser, Address 


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        PREPARING = "PREPARING", "Preparing"
        READY = "READY", "Ready"
        DELIVERING = "DELIVERING", "Delivering"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    address = models.ForeignKey(Address, on_delete=models.PROTECT) # for both user and address: should i create multiple order attributes related to the order model to snapshot its values or use on_delete=models.PROTECT?


    def update_total_price(self):
        total = sum(item.subtotal for item in self.items.all())

        self.total_price = total
        self.save(update_fields=["total_price"])


    ''' TO-DO:
        - direct status assignment still possible outside transition methods
        - example: order.status = Order.Status.COMPLETED -> order.save()
        - build a generic function? it would receive a state as parameter. could avoid repetition too 
    '''

    def confirm_order(self):
        if self.status != self.Status.PENDING:
            raise ValidationError("Only pending orders can be confirmed.")
        
        if not self.items.exists():
            raise ValidationError("Cannot confirm an order without items")
        
        if self.total_price < 30:
            raise ValidationError("The total price should be R$30,00 or more.")
        
        self.status = self.Status.CONFIRMED
        self.save(update_fields=["status"])
    

    def start_order(self):
        if self.status != self.Status.CONFIRMED:
            raise ValidationError("Only confirmed orders can be started.")
        
        self.status = self.Status.PREPARING
        self.save(update_fields=["status"])
    
    
    def mark_ready(self):
        if self.status != self.Status.PREPARING:
            raise ValidationError("Only preparing orders can be marked as ready.")
        
        self.status = self.Status.READY
        self.save(update_fields=["status"])
    

    def start_delivery(self):
        if self.status != self.Status.READY:
            raise ValidationError("Only ready orders can be marked as delivering.")
        
        self.status = self.Status.DELIVERING
        self.save(update_fields=["status"])
    

    def complete_order(self):
        if self.status != self.Status.DELIVERING:
            raise ValidationError("Only delivering orders can be marked as completed.")

        self.status = self.Status.COMPLETED
        self.save(update_fields=["status"])


    def cancel_order(self):
        if self.status not in [self.Status.PENDING, self.Status.CONFIRMED]:
            raise ValidationError("Only pending or confirmed orders can be cancelled.")
        
        self.status = self.Status.CANCELLED
        self.save(update_fields=["status"])


    def __str__(self):
        return f"Order #{self.id} - {self.status}"


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