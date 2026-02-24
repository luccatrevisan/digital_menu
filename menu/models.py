from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=300, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='menu_photos/%Y/', blank=False, null=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        if self.old_price is not None and self.old_price <= self.price:
            raise ValidationError("Invalid price.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Stock(models.Model):
    menu_item = models.OneToOneField(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.quantity}"


class Complement(models.Model): # should it have a complement_group field?
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ComplementGroup(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    min_quantity = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0)])
    max_quantity = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)]) #change? ta certo?
    complements = models.ManyToManyField(Complement)

    def __str__(self):
        return self.name

    def clean(self):
        if self.min_quantity > self.max_quantity:
            raise ValidationError("The minimum quantity must be less than the maximum.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)