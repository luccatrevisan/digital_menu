from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from apps.menu.utils import normalize_name, normalize_description


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        self.name = normalize_name(self.name)
        if self.description: #since its optional (null=True).
            self.description = normalize_description(self.description)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



class MenuItem(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=300, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, validators=[MinValueValidator(0.01)])
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='menu_photos/%Y/', blank=False, null=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        if self.old_price is not None and self.old_price <= self.price:
            raise ValidationError("Invalid price.")
        
        self.name = normalize_name(self.name)
        self.description = normalize_description(self.description)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Stock(models.Model):
    menu_item = models.OneToOneField(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.quantity}"


class Complement(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def clean(self):
        self.name = normalize_name(self.name)
        if self.description: #since its optional.
            self.description = normalize_description(self.description)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ComplementGroup(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    min_quantity = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0)])
    max_quantity = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])
    complements = models.ManyToManyField(Complement)

    def __str__(self):
        return self.name

    def clean(self):
        if self.min_quantity > self.max_quantity:
            raise ValidationError("The minimum quantity must be less than the maximum.")
    
        self.name = normalize_name(self.name)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)