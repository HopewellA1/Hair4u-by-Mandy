"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('cartTemp', views.cartTemp, name="cartTemp")
    
    
]
