from django.contrib import admin
from .models import Product,Cart,UserAddress1,PaytmHistory,CheckOut
# Register your models here.
admin.site.register(Product);
admin.site.register(Cart);
admin.site.register(UserAddress1);
admin.site.register(PaytmHistory);
admin.site.register(CheckOut);