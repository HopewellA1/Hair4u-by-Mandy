from django.db import models
from django.contrib.auth.models import User 


class Estore(models.Model):
    EstorId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    EstoreName = models.CharField(blank=False,max_length=60)
    PhoneNumber = models.CharField(blank=False, max_length=15, null=False)
    EmailAddress = models.CharField(blank=False, null=False, max_length=60)
    Address = models.TextField(blank=True,null=True,max_length=100)
    Type = models.CharField(blank=False, null=False,max_length=60)
    Description = models.TextField(blank=False, null=False,max_length=300)
    ApprovalSataus = models.CharField(blank=False,null=False, default="Pending",max_length=15)#Super user will approve to e_store to operate if the product sold is legal and not harfull anyhow 
    Status = models.CharField(blank=False, null=False, default="Pending", max_length=15)#This one indicates if the store is operational or not they will have to be checked after 3 months or so if they are still using the app or not
    NumberOfItems = models.IntegerField(default=0)
    TsAndCsAccepted = models.BooleanField(default=False)#User must accept all terms and conditions in order to use the application
    CreatDate= models.DateTimeField()
    
    
class Finance(models.Model):
    FinanceId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    EstorId = models.ForeignKey(Estore,blank=True,null=True,on_delete=models.CASCADE)
    TotalItemsSold = models.IntegerField()
    EstoreProfit = models.CharField(blank=False, null=False,max_length=22)
    TotalInvestment =  models.CharField(blank=False, null=False,max_length=22)
     
class Item(models.Model):
    ItemId  = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    EstorId = models.ForeignKey(Estore,blank=True,null=True,on_delete=models.CASCADE)
    AddeBy = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    ItemName = models.CharField(blank=False, null=False, max_length=60)
    Price = models.DecimalField(blank=False, null=False,max_digits=20,decimal_places=2)
    BuyPrice = models.CharField(blank=False, null=False,max_length=22)
    Profit = models.CharField(blank=False, null=False,max_length=70, default='0')
    Investament = models.CharField(blank=False, null=False,max_length=70)
    NumSold = models.IntegerField()
    Quantity = models.IntegerField()
    Status = models.CharField(blank=False, null=False, max_length=15, default='Available')
    ExpDate = models.CharField(max_length=60,default="Not applicable")
    ItemVisual = models.FileField(blank=False,null=False,upload_to='StorManager/itemImages')
    ItemDescription = models.TextField(blank=False, null=False,max_length=300, default="Describe")
    ItemType = models.CharField(null=False, blank=False, default="default", max_length=20)
    
    
    
class PackageItem(models.Model):
    PackageItemId =  models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    ItemId = models.ForeignKey(Item,blank=True,null=True,on_delete=models.CASCADE)
    PackageItemName = models.CharField(blank=False, null=False, max_length=60)
    Price =  models.DecimalField(blank=False, null=False,max_digits=20,decimal_places=2)
    Quantity = models.IntegerField(default=1)
    

    

    
    