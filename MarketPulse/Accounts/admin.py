from django.contrib import admin

# Register your models here.
from .models import Consumer, ShopOwner, Product
admin.site.register(Consumer)
admin.site.register(ShopOwner)
admin.site.register(Product)
