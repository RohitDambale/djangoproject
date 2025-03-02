from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Msg(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.BigIntegerField()
    msg=models.CharField(max_length=200)

class Product(models.Model):
    cat=((3,'Samsung'),(1,'Iphone'),(2,'Oneplus'))
    name=models.CharField(max_length=40,verbose_name="product name")
    price=models.FloatField()
    pdetails=models.CharField(max_length=100,verbose_name="product details")
    cat=models.BigIntegerField(verbose_name="category",choices=cat)
    is_activate=models.BooleanField(default=True,verbose_name="available")
    pimage=models.ImageField(upload_to='image')

    def __str__(self):
        return self.name

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
    
class Order(models.Model):
    order_id=models.CharField(max_length=50)
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    qty=models.IntegerField(default=1)