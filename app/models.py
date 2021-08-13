from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

from django.contrib.auth.models import User
# Create your models here.
class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True,null=True)
    first_name=models.CharField(max_length=30,null=True)
    last_name=models.CharField(max_length=30,null=True)
    password=models.CharField(max_length=300)
    is_staff=models.BooleanField(default=True)
    #is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    USERNAME_FIELD='email'
    objects=UserManager()
    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    seen = models.BooleanField(default=False)
    

class UserOTP(models.Model):
	user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
	time_st = models.DateTimeField(auto_now = True)
	otp = models.SmallIntegerField()