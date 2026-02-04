from django.db import models


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
    image = models.ImageField(upload_to='menu_photos/%Y/', blank=False, null=False)

    def __str__(self):
        return self.name
    

class Stock(models.Model):
    menu_item = models.OneToOneField(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} unidades disponíveis."