from django.contrib import admin

# Register your models here.
from .models import  Region, Product, Client, SalesMan,Transaction
admin.site.register(Region)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(SalesMan)

admin.site.register(Transaction)
