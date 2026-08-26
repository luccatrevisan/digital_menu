from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True) 


class Address(models.Model):
    LABEL_CHOICES = [
        ('CASA', 'Casa'),
        ('TRABALHO', 'Trabalho')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    cep = models.CharField(max_length=8, null=False, blank=False)
    street = models.CharField(max_length=255, null=False, blank=False)
    number = models.CharField(max_length=20, null=False, blank=False)
    complement = models.CharField(max_length=255, null=True, blank=True) 
    neighborhood = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=2, null=False, blank=False)
    label = models.CharField(max_length=50, choices=LABEL_CHOICES, null=True, blank=True) 

    def __str__(self):
        return f'{self.street}, {self.number} - {self.city}/{self.state}'