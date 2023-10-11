from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('createEstore', views.createEstore,name="createEstore"),
    path('addItem', views.addItem, name="addItem"),
    path('ItemUpdate/<int:itemId>', views.ItemUpdate, name="ItemUpdate"),
    
    path('itemDetails/<int:itemId>',views.itemDetails, name="itemDetails"),
    path('ItemsList', views.ItemsList, name ="ItemsList"),
    path('DeleteItem/<int:ItemId>', views.DeleteItem, name="DeleteItem"),
    path('EstoreAbout', views.EstoreAbout, name="EstoreAbout"),
    path('updateEstore', views.updateEstore, name="updateEstore"),
    path('cartTemp', views.cartTemp, name="cartTemp"),
    path('addPackageItem/<int:itemId>', views.addPackageItem, name="addPackageItem"),
    path('PackageItemUpdate/<int:PackageItemId>', views.PackageItemUpdate, name="PackageItemUpdate"),
    path('DeletePackageItem/<int:packageItemId>', views.DeletePackageItem, name="DeletePackageItem"),
    path('creatDeletePackageItem/<int:packageItemId>', views.creatDeletePackageItem, name="creatDeletePackageItem"),
    
    
    
]
