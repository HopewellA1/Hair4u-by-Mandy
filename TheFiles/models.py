from django.db import models
from django.contrib.auth.models import User



class EstorLogo(models.Model):
    EstorId = models.IntegerField(primary_key=True,blank=False,null=False)
    Logo = models.FileField(upload_to='TheFiles/files',blank=True, null=True)
    
class ItemVisual(models.Model):
    ItemId = models.IntegerField(primary_key=True,blank=False,null=False)
    Visual =  models.FileField(upload_to='TheFiles/files',blank=True, null=True)
    