from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('createOrder/<int:itemId>', views.createOrder, name="createOrder"),
    path('GetOrderNumItems', views.GetOrderNumItems, name="GetOrderNumItems"),
    path('cart', views.cart, name="cart"),
    path('removeCartItem/<int:OrderItemId>', views.removeCartItem, name="removeCartItem"),
    path('clearCart', views.clearCart, name="clearCart"),
    path('AddOrderPackageItem/<int:itemId>', views.AddOrderPackageItem, name="AddOrderPackageItem"),
    path('RemoveOrderPackageItem/<int:packageItemOrderId>', views.RemoveOrderPackageItem, name="RemoveOrderPackageItem"),
    path('purchaseFullPack/<int:OrderItemId>', views.purchaseFullPack, name="purchaseFullPack"),
    path('Checkout/<int:orderId>', views.Checkout, name="Checkout"),
    path('Approve/<int:orderId>', views.Approve, name="Approve"),
    path('Orders', views.Orders, name="Orders")
    
    
]
