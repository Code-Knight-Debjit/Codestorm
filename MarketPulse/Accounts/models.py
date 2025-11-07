from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields for consumer details
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

class ShopOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields for shop owner details
    shop_name = models.CharField(max_length=255)
    shop_address = models.CharField(max_length=255)
    shop_phone_number = models.CharField(max_length=20)
    def __str__(self):
        return self.shop_name

class Product(models.Model):
    shop_owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
