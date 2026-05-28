from decimal import Decimal
from django.db import models
from apps.menu.models import MenuItem, Complement, ComplementGroup
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from apps.users.models import CustomUser, Address 


class Order(models.Model):
    class Status(models.TextChoices):
        '''
        ORDER STATUSES
            - PENDING: in practice, its the CART. the user is creating the order.
            - CONFIRMED: the user finished the order. it may not mean that the user payed for the order, since more problems could happen between confirming and successfully paying. in the future, it opens space to payment-related statuses
            - PREPARING: everything is ok. cookies going to the oven.
            - READY: everything is ready to go.
            - DELIVERING: the order left the house.
            - COMPLETED: the order sucessfully arrived to the hands of the customer.
            - CANCELLED: allowed, but only before the start of the order (business rule)
        '''

        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        PREPARING = "PREPARING", "Preparing"
        READY = "READY", "Ready"
        DELIVERING = "DELIVERING", "Delivering"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
    

    class DeliveryType(models.TextChoices):
        PICKUP = "PICKUP", "Pickup"
        DELIVERY = "DELIVERY", "Delivery"


    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    delivery_type = models.CharField(max_length=20, choices=DeliveryType.choices, default=DeliveryType.DELIVERY)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    # snapshot fields to maintain delivery address data.
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="orders", null=True, blank=True)
    delivery_cep = models.CharField(max_length=9, null=True, blank=True)
    delivery_street = models.CharField(max_length=255, null=True, blank=True)
    delivery_number = models.CharField(max_length=20, null=True, blank=True)
    delivery_complement = models.CharField(max_length=255, null=True, blank=True) 
    delivery_neighborhood = models.CharField(max_length=100, null=True, blank=True)
    delivery_city = models.CharField(max_length=100, null=True, blank=True)
    delivery_state = models.CharField(max_length=2, null=True, blank=True)
    delivery_label = models.CharField(max_length=50, null=True, blank=True) 


    def update_total_price(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_price = total
        self.save(update_fields=["total_price"])


    def populate_delivery_fields(self):
        '''
        populates the fields related to the delivery address with information about the user's address 
            - for each field from address, it snapshots its values to keep the historical data intact
            - if the user changes the address, the database will keep the original values 
            - data-driven architecture for possible analysis  
        '''
        self.delivery_cep = self.address.cep
        self.delivery_street = self.address.street
        self.delivery_number = self.address.number
        self.delivery_complement = self.address.complement
        self.delivery_neighborhood = self.address.neighborhood
        self.delivery_city = self.address.city
        self.delivery_state = self.address.state
        self.delivery_label = self.address.label


    ''' 
    TO-DO:
        - direct status assignment still possible outside transition methods
        - example: order.status = Order.Status.COMPLETED -> order.save()
    '''

    def _transition_to(self, new_status):
        self.status = new_status
        self.save()


    def confirm_order(self):
        if self.status != self.Status.PENDING:
            raise ValidationError("Only pending orders can be confirmed.")
        
        if not self.items.exists():
            raise ValidationError("Cannot confirm an order without items.")
        
        if (self.delivery_type == self.DeliveryType.DELIVERY and self.address is None):
            raise ValidationError("Delivery orders require an address.")
        
        if self.total_price < 30:
            raise ValidationError("The total price should be R$30,00 or more.")
        
        if self.delivery_type == self.DeliveryType.DELIVERY:
            self.populate_delivery_fields()
        self._transition_to(self.Status.CONFIRMED)
    

    def start_preparing(self):
        if self.status != self.Status.CONFIRMED:
            raise ValidationError("Only confirmed orders can be started.")
        
        self._transition_to(self.Status.PREPARING)
    
    
    def mark_ready(self):
        if self.status != self.Status.PREPARING:
            raise ValidationError("Only preparing orders can be marked as ready.")
        
        self._transition_to(self.Status.READY)
    

    def start_delivery(self):
        if self.status != self.Status.READY:
            raise ValidationError("Only ready orders can be marked as delivering.")
        
        self._transition_to(self.Status.DELIVERING)
    

    def complete_order(self):
        if self.status != self.Status.DELIVERING:
            raise ValidationError("Only delivering orders can be marked as completed.")

        self._transition_to(self.Status.COMPLETED)


    def cancel_order(self):
        if self.status not in [self.Status.PENDING, self.Status.CONFIRMED]:
            raise ValidationError("Only pending or confirmed orders can be cancelled.")
        
        self._transition_to(self.Status.CANCELLED)


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