from django.db import models
from django.contrib.auth.models import User 
from StorManager.models import Estore, Item, PackageItem
from datetime import date, datetime



class Order(models.Model):
    OrderId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)#Customer
    numItems = models.IntegerField(default=0)# number of item on the cart
    Amount = models.DecimalField(blank=False, null=False,max_digits=20,decimal_places=2)
    status = models.CharField(blank=False, null=False, max_length=30, default='Available')
    
    createDate = models.DateTimeField()
    
    
    
class OrderItem(models.Model):
    OrderItemId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    OrderId = models.ForeignKey(Order,blank=True,null=True,on_delete=models.CASCADE)
    itemId = models.ForeignKey(Item,blank=True,null=True,on_delete=models.CASCADE)
    DateSelect = models.DateTimeField(default=datetime.now())
    ItemType = models.CharField(null=False, blank=False, default="default", max_length=20)
    PartOrFull =  models.CharField(null=False, blank=False, default="FullPackage", max_length=20)
    packPrice = models.DecimalField(blank=False, null=False,max_digits=20,decimal_places=2, default=0.00)
    
    
class PackageItemOrder(models.Model):
    PackageItemOrderId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    PackageItemId = models.ForeignKey(PackageItem,blank=True,null=True,on_delete=models.CASCADE)
    OrderItemId = models.ForeignKey(OrderItem,blank=True,null=True,on_delete=models.CASCADE)
    
    
    


