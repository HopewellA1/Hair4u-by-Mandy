from datetime import date, datetime
import requests
import os
from rest_framework import status   
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrderSerializer,OrderItemSerializer,PackageItemOrderSerializer
#from . models import ItemVisual,EstorLogo
from django.contrib import messages
from StorManager.models import Item,Estore,PackageItem
from .models import Order, OrderItem, PackageItemOrder
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site






@login_required
def createOrder(request, itemId):
    
    user = request.user
    try:
        NewOrder = get_object_or_404(Order, user = user,status="OnCreate")   
    except:
        
        
        NewOrder = Order.objects.create(
            user = user,
            numItems = 0,
            Amount = 0.00,
            status = 'OnCreate',
            createDate = datetime.now()
        )
        messages.success(request, "You order has been created successfully, check your cart for further details")
        
    orderItem = addOrderItem(NewOrder.OrderId, int(itemId))
    if orderItem.ItemType =='package':
        messages.warning(request, "This is a package item please specify which items you prefer.")
        return redirect("AddOrderPackageItem", itemId = orderItem.OrderItemId)
    messages.success(request, "Item added to cart.")
    
    return redirect("ItemsList")



def addOrderItem(orderId, itemId):
    print("in order")
    order = get_object_or_404(Order, pk = orderId)
    item = get_object_or_404(Item, pk = itemId)
    
    orderItem = OrderItem.objects.create(
        OrderId = order,
        itemId = item,
       # DateSelect = datetime.now(),
        ItemType = item.ItemType,
        
    )
    order.numItems = countItems(OrderItem.objects.filter(OrderId = order))
    if orderItem.ItemType != "package":
        order.Amount += item.Price
        
    
    order.save()
    return orderItem
    



def AddOrderPackageItem(request,itemId):
    
    orderItem = get_object_or_404(OrderItem, pk = itemId)
    packItems = PackageItem.objects.filter(ItemId =orderItem.itemId )
    order = orderItem.OrderId
    selectedItems = PackageItemOrder.objects.filter(OrderItemId = orderItem)
    selectedItemsCount = countItems(selectedItems)
    if request.method =='GET':
        domain = get_current_site(request).domain
        return render(request, 'ManageOrder/AddOrderPackageItem.html',{"orderItem":orderItem, "PackageItems":packItems, "selectedItems":selectedItems,"selectedItemsCount":selectedItemsCount, "domain":domain})
    
    
    if request.method=='POST':
        selectedPackItem = get_object_or_404(PackageItem, pk = int(request.POST["PackageItemOrderId"]))
        packageItemOrder = PackageItemOrder.objects.create(
            PackageItemId = selectedPackItem,
            OrderItemId = orderItem
        )
        order.Amount += selectedPackItem.Price
        orderItem.packPrice +=selectedPackItem.Price
        orderItem.PartOrFull="part"
        order.save()
        orderItem.save()
        
        messages.success(request, 'Pack item added successfully. Scroll down to see selected items')
        return redirect("AddOrderPackageItem",itemId = orderItem.OrderItemId)


def purchaseFullPack(request, OrderItemId):
    orderItem = get_object_or_404(OrderItem, pk = OrderItemId)
    order = orderItem.OrderId
    item = orderItem.itemId
    orderItem.PartOrFull="full"
    
    order.Amount += item.Price
    orderItem.save()
    order.save()
    messages.success(request, "Item added to cart as full package. You may continue with your shopping.")
    return redirect("ItemsList")
    
    
    
def  RemoveOrderPackageItem(request,packageItemOrderId ):
    
    packageItemOrder = get_object_or_404(PackageItemOrder, pk = packageItemOrderId)
    orderItem = packageItemOrder.OrderItemId
    order = orderItem.OrderId
    
    order.Amount -= packageItemOrder.PackageItemId.Price
    orderItem.packPrice -=packageItemOrder.PackageItemId.Price
        
    order.save()
    orderItem.save()
    packageItemOrder.delete()
    messages.success(request, 'Pack item removed successfully')
    return redirect("AddOrderPackageItem",itemId = orderItem.OrderItemId)
    
    
    
    
       
#by customer
@api_view(['POST', 'GET'])
@login_required
def GetOrderNumItems(request):
    
    numItems = 0
    user = request.user
    try:
        order = get_object_or_404(Order, user = user,status="OnCreate")
        numItems = order.numItems
    except:
        pass
    
    
    return Response({"numItems": numItems})


    
    
def countItems(list):
    
    count = 0
    
    for item in list:
        count +=1
        
    return count


@login_required
def cart(request):
    
    user = request.user
    order = None
    try:
        order = get_object_or_404(Order, user = user,status="OnCreate")
       
    except:
        try:
            order = get_object_or_404(Order, user = user,status="Pending")
            
        except:
            try:
                order = get_object_or_404(Order, user = user,status="Approved")
                 
            except:
                pass
            pass
        messages.info(request,'You do not have any items on your cart at memoment. To create a cartr please navigate to "Sell items" on the top manu and select items you would like to purchase.')
        pass
    
    OrderItems = OrderItem.objects.filter(OrderId = order, ItemType ="default" )
    domain = get_current_site(request).domain
    PackageItems = getPackageItems(OrderItem.objects.filter(OrderId = order, ItemType ="package" ))
    
    return render(request, 'ManageOrder/cart.html', {"order": order,"OrderItems":OrderItems , "domain":domain, "PackageItems":PackageItems})
    
  
def getPackageItems(PackageItems):
    packList = []
    for item in PackageItems:
        selected = PackageItemOrder.objects.filter(OrderItemId  =item)
        packList.append({"Item":item, "selected":selected })
    return packList



def removeCartItem(request, OrderItemId):
    
    orderItem = get_object_or_404(OrderItem, pk = OrderItemId )
    order = orderItem.OrderId
    order.numItems -=1
    order.Amount -= orderItem.itemId.Price
    order.save()
    orderItem.delete()
    
    messages.success(request, 'Item removed from cart successfully')
    
    return redirect("cart")


@login_required
def clearCart(request):
    user = request.user
    try:
        order = get_object_or_404(Order, user = user,status="OnCreate")  
    except:
        messages.info(request,'You do not have any items on your cart at memoment. To create a cart please navigate to "Sell items" on the top manu and select items you would like to purchase.')
        return redirect("cart")
        pass
    order.delete()
    messages.success(request, "The cart was cleared successfully.")
    return redirect("cart")

def Checkout(request, orderId):
    
    user = request.user
    order = None
    order = get_object_or_404(Order,pk= orderId)
    order.status= "Pending"
    order.save()
    messages.success(request, "The order has been checked out successfully and is waiting admin approval.")
    OrderItems = OrderItem.objects.filter(OrderId = order, ItemType ="default" )
    OrderItems = OrderItem.objects.filter(OrderId = order, ItemType ="default" )
    domain = get_current_site(request).domain
    PackageItems = getPackageItems(OrderItem.objects.filter(OrderId = order, ItemType ="package" ))
    return render(request, 'ManageOrder/cart.html', {"order": order,"OrderItems":OrderItems , "domain":domain, "PackageItems":PackageItems})
def Orders(request):
    
    Pendingorders = Order.objects.filter(status="Pending")
    ApprovedOrders = Order.objects.filter(status="Approved")
    
    return render(request, 'ManageOrder/Orders.html', {"Pendingorders":Pendingorders,"ApprovedOrders":ApprovedOrders})
def Approve(request, orderId):
    
    user = request.user
    order = None
    order = get_object_or_404(Order,pk= orderId)
    order.status= "Approved"
    order.save()
    messages.success(request,"Order has been approved.")
    OrderItems = OrderItem.objects.filter(OrderId = order, ItemType ="default" )
    OrderItems = OrderItem.objects.filter(OrderId = order, ItemType ="default" )
    domain = get_current_site(request).domain
    PackageItems = getPackageItems(OrderItem.objects.filter(OrderId = order, ItemType ="package" ))
    return render(request, 'ManageOrder/cart.html', {"order": order,"OrderItems":OrderItems , "domain":domain, "PackageItems":PackageItems})










# def getPackAddingState(OrderItemId):
    
    
#     res = False
    
#     orderItem = get_object_or_404(OrderItem, pk = OrderItemId)
#     item = orderItem.itemId
    
#     numSelected = countItems(PackageItemOrder.objects.filter(OrderItemId =orderItem ))
#     packItem = countItems(PackageItem.objects.filter(ItemId=item))
#     if 


    
    
    
    
    
    
    
    

    
    

    
    
    
    


