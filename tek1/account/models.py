from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from datetime import date
from django.utils import timezone

class User(AbstractUser):
    is_recep = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(max_length=70,blank=True ,unique=True)

class Temp(models.Model):
    uid=models.CharField(max_length=50)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    pincode=models.IntegerField(default=245101)
    purpose=models.CharField(blank=True,max_length=1000)
    gender=models.CharField(max_length=100)
    dob=models.CharField(default="05-05-1996",max_length=200)

class Visitor_perma(models.Model):
    uid=models.CharField(max_length=50)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    email=models.CharField(blank=True,max_length=70)
    phone=models.BigIntegerField()
    dob=models.CharField(default="05-05-1996",max_length=200)
    pincode=models.IntegerField(default=245101)
    purpose=models.CharField(blank=True,max_length=1000)
    whoto=models.CharField(blank=True, max_length=50)
    date=models.DateTimeField(default=timezone.now,blank=True,null=True)
