from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)


class Address(models.Model):
    LABEL_CHOICES = [
        ('CASA', 'Casa'),
        ('TRABALHO', 'Trabalho')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')

    cep = models.CharField(max_length=9) # TO-DO: CEP is the zip code in Brazil. if it is the first field to be filled, make that the other ones be automatically filled based on its value

    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    complement = models.CharField(max_length=255, blank=True) 
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    label = models.CharField(max_length=50, choices=LABEL_CHOICES) 

    def __str__(self):
        return f'{self.street}, {self.number} - {self.city}/{self.state}'