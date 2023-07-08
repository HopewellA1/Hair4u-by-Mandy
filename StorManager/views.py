from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from .models import Estore,Finance,Item
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.sites.shortcuts import get_current_site
from TheFiles.models import ItemVisual
from TheFiles.views import delete_file_from_field


def home(request):
    

    return render(request, 'StorManager/home.html')







@login_required
def createEstore(request):
    user =  request.user
    if request.method == 'GET':
        
        return render(request, 'StorManager/createEstor.html')

    if request.method =='POST':
        tcs = False
        if request.POST["TsAndCsAccepted"] == "Accepted":
            tcs = True
        estore = Estore.objects.create(
            user = user,
            EstoreName = request.POST["EstoreName"],
            PhoneNumber = request.POST["PhoneNumber"],
            EmailAddress = request.POST["EmailAddress"],
            Address = request.POST["Address"],
            Type = request.POST["Type"],
            Description = request.POST["Description"],
            TsAndCsAccepted= tcs,
            CreatDate = datetime.now()
            
            
        )
        estoreFinance = Finance.objects.create(
            EstorId = estore,
            TotalItemsSold ='0',
            EstoreProfit = '0',
            TotalInvestment = '0'
            
        )
        messages.success(request, "E_store information added successfully please proceed to add Items")
        return redirect("addItem")
        
@login_required
def addItem(request):
    user = request.user
    estore = None
    items = []
    try: 
        estore = get_object_or_404(Estore, user= user)
        items = Item.objects.filter(EstorId = estore)
    except:
        return HttpResponse("You can not add any items the Estore you are refering to is NOT FOUND")
    
    user =  request.user
    
    if  request.method =='GET':
        domain = get_current_site(request).domain
      
        return render(request, 'StorManager/addItem.html', {"items":items, "domain":domain})
    
    
    if request.method == 'POST':
        
        user =  request.user
        item = Item.objects.create(
            EstorId = estore,
            AddeBy = user,
            ItemName = request.POST["ItemName"],
            Price = request.POST["Price"],
            BuyPrice = 'None',
            Investament = '0',
            NumSold = 0,
            Quantity = request.POST["Quantity"],
         
            ItemVisual = request.FILES["ItemVisualIput"],
            ItemDescription = request.POST["ItemDescription"],
            
        )
        msg = "Item has been added successfully on estore."
    #     file = {
    #                 'Visual':request.FILES["ItemVisualIput"],
    #             }
                            
    #     payload ={
    #                 'ItemId':item.ItemId,
    #             }
    #     domain = get_current_site(request).domain
    #     url = "https://"+domain+"/TheFilesItemVisualCreate/"
    #    # url = "{% url 'ItemVisualUpdate' itemId=%}"
    #     r = requests.post(url, data = payload,files=file)
        
    #     #{'ItemId': 10, 'Visual': '/media/TheFiles/files/Screenshot_2023-03-11_053952.png'}
    #     print(r.status_code)
    #     data = r.json()
    #     if r.status_code == 200:
    #         item.ItemVisual = data["Visual"]
    #         item.save() 
    #         msg += " And the item image is saved succefully on the database."
    #     else:
    #         msg += " And the was a problem saving the image, error: "+r.status_code  
        
        
       
        messages.success(request, msg)
        return redirect("addItem")
    
@login_required   
def ItemUpdate(request, itemId):
    # we will use this as the whole item update page
    try:
        item = get_object_or_404(Item, pk = itemId)
        
    except:
        return HttpResponse("The Item you tried to access is not found please proceed to add it")
    
    if request.method =='GET':
       
        domain = get_current_site(request).domain
        return render(request, 'StorManager/ItemVisualUpdate.html', {"item":item, "domain":domain})
    
    if request.method == 'POST':
        
        
        numUpdate = 0
        if request.POST["ItemName"] != item.ItemName:
            print("ItemName")
            item.ItemName = request.POST["ItemName"]
            numUpdate +=1

        
        if request.POST["Price"] != item.Price:
            print("Price")
            item.Price = request.POST["Price"]
            numUpdate +=1
        
        if int(request.POST["Quantity"]) != item.Quantity:
            print(request.POST["Quantity"])
            print(item.Quantity)
            print("Quantity")
            item.Quantity = request.POST["Quantity"]
            numUpdate+=1
            
        if request.POST["ItemDescription"] != item.ItemDescription :
            print("ItemDescription")
            item.ItemDescription = request.POST["ItemDescription"]
            numUpdate += 1
        
       
    
        #image updating
        try:
            if request.FILES["ItemVisualIput"]:
                delete_file_from_field(item, 'ItemVisual')
                item.ItemVisual = request.FILES["ItemVisualIput"]
                numUpdate += 1
                    # file = {
                    #             'Visual':request.FILES["ItemVisualIput"],
                    #         }
                                        
                    # payload ={
                    #             'ItemId':item.ItemId,
                    #         }
                    # domain = get_current_site(request).domain
                    # url = "http://"+domain+"/TheFilesItemVisualUpdate/"+str(item.ItemId)

                    # r = requests.post(url, data = payload,files=file)
                    # #data = r.json()
                    # print("request status: "+str(r.status_code))
                    # if r.status_code == 200:
                        
                    #     messages.success(request,"Item image is updated succefully on the database.")
                        
                    # else:
                    #     messages.error(request,"The was a problem saving the image, error: "+str(r.status_code))  
            
        except:
            pass
        if numUpdate > 0:
                
            item.save()
            messages.success(request, f"{numUpdate} changes saved successfully")   
        else:
                messages.warning(request, "No changes made")        
            
     
            
        
            
    return redirect("itemDetails", itemId =item.ItemId )


@login_required
def itemDetails(request, itemId):
    
    try:
        item = get_object_or_404(Item, pk = itemId)
        
    except:
        return HttpResponse("The Item you tried to access is not found please proceed to add it")
    domain = get_current_site(request).domain
    return render(request, 'StorManager/itemDetails.html', {"item":item,"estore":item.EstorId,"domain":domain})

@login_required
def estoreDetails(request, estoreId):
    
    try:
        estore = get_object_or_404(Estore, pk = estoreId)
        items = Item.objects.filter(EstorId =estore)
    except:
        return HttpResponse("The estore you tried to aceess is not found please proceed to make a request for one, ont the create estor page")
    
    return render(request, 'StorManager/estoreDetails.html', {"estore":estore, "items":items})
        
        
@login_required 
def ItemsList(request):
    items = Item.objects.filter(Status = 'Available')
    
    domain = get_current_site(request).domain
    return render(request, 'StorManager/ItemsList.html',{"items":items,"domain":domain})



@login_required
def DeleteItem(request, ItemId):
    user = request.user
     
    item = get_object_or_404(Item, pk = ItemId)
    estore = item.EstorId
    
    if user!= estore.user:
        return HttpResponse("The Action you are trying to commit is for the owner. and your're not yeka nje ungazami ngoba uzoblokeka, cela singaphaphelani.")
    
    if request.method == 'GET':
        domain = get_current_site(request).domain
        messages.warning(request, "If one or more orders has been made on the Item it will not be romoved fully, but the image will be removed for storage reuse.")
        return render(request, 'StorManager/DeleteItem.html', {"item":item, "domain":domain})
    
    
    if request.method == 'POST':
        
        delete_file_from_field(item, 'ItemVisual')
        item.delete()
        
        messages.success(request, "The item has been deleted successfully, you may add more.")
        
        return redirect('addItem')
    
    
    
def EstoreAbout(request):
    
    estore = get_object_or_404(Estore, pk =3)
    
    return render( request,'StorManager/EstoreAbout.html', {"estore":estore})


@login_required
def updateEstore(request):
    user  = request.user
    try:
        estore = get_object_or_404(Estore, user=user)    
        
    except:
        return HttpResponse("You are acceing pages you must not. Awuhlale lapho obekwe khona ungahambe ungena nje, cela singaphaphelani please.")
    
    if request.method =='GET':
        
        return render(request, 'StorManager/updateEstore.html',{"estore":estore} )
    
    
    if request.method == 'POST':
        numUpdates = 0
        if request.POST["EstoreName"] != estore.EstoreName:
            estore.EstoreName = request.POST["EstoreName"]
            numUpdates += 1
            
        if request.POST["PhoneNumber"] != estore.PhoneNumber:
            
            estore.PhoneNumber = request.POST["PhoneNumber"]
            numUpdates += 1
            
        if request.POST["EmailAddress"] != estore.EmailAddress:
            
            estore.EmailAddress = request.POST["EmailAddress"]
            numUpdates += 1
        
        if request.POST["Address"] != estore.Address:
            
            estore.Address = request.POST["Address"]
            numUpdates += 1
        if request.POST["Description"] != estore.Description:
            
            estore.Description = estore.Description
            numUpdates += 1
            
        if numUpdates > 0 :
            estore.save()
            messages.success(request, "The changes were saves successfully.") 
        else:
            messages.warning(request, "There no changes made.")    
        
            
        return redirect('EstoreAbout')   
    
    
    
def cartTemp(request):
    
    messages.warning(request, "Please note that this is the page where the user will see what they have ordered. The orders functionality is yet to be implemented.")
        
    return render(request, 'StorManager/cartTemp.html')
    
    
    
    