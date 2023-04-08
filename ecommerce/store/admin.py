from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Customer)    #это добавляем базы данных в джанго админку
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
