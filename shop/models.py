from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
# Create your models here.
class Product(models.Model):
    id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=300)
    product_image=models.ImageField(upload_to="media/",default="images/bck.jpg")
    product_type=models.CharField(max_length=400)
    product_manufacture=models.CharField(max_length=500)
    product_price=models.CharField(max_length=500)
    def __str__(self):
        return str(self.id);
class Cart(models.Model):
    id=models.AutoField(primary_key=True)
    user_email=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    status=models.BooleanField(default=True)
    
class UserAddress1(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address=models.CharField(max_length=3000)
    #status=models.BooleanField(default=False) 
    
from django.utils import timezone
# Create your models here.

class CheckOut(models.Model):
    id=models.AutoField(primary_key=True)
    #cart=models.ForeignKey(Cart,on_delete=models.CASCADE,default="")
    user_email=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default="")
    product_id=models.CharField(max_length=3000,default="")
    address=models.CharField(max_length=3000,default='')
    quantity=models.CharField(max_length=3000,default="")
    status=models.BooleanField(default=False)
    
class PaytmHistory(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default="")
   # product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
#    checout=models.ForeignKey(CheckOut,on_delete=models.CASCADE,default="")
   # address=models.ForeignKey(UserAddress1,on_delete=models.CASCADE,default="")
    quantity=models.FloatField(default=0.0,null=True)
    ORDERID = models.CharField('ORDER ID', max_length=30)
    TXNDATE = models.DateField('TXN DATE',auto_now_add=True)
    TXNID = models.CharField('TXN ID',max_length=3000)
    BANKTXNID = models.IntegerField('BANK TXN ID', null=True, blank=True)
    BANKNAME = models.CharField('BANK NAME', max_length=50, null=True, blank=True)
    RESPCODE = models.IntegerField('RESP CODE')
    PAYMENTMODE = models.CharField('PAYMENT MODE', max_length=10, null=True, blank=True)
    CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True)
    GATEWAYNAME = models.CharField("GATEWAY NAME", max_length=30, null=True, blank=True)
    MID = models.CharField(max_length=40)
    RESPMSG = models.TextField('RESP MSG', max_length=250)
    TXNAMOUNT = models.FloatField('TXN AMOUNT')
    STATUS = models.CharField('STATUS', max_length=12)

    class Meta:
        app_label = 'shop'

    def __unicode__(self):
        return self.STATUS 