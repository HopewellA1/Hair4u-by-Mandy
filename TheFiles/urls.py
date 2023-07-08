from django.urls import path
from . import views




urlpatterns = [
 
    path('ItemVisualCreate/', views.ItemVisualCreate, name="ItemVisualCreate"),
    path('EstorLogoCreate', views.EstorLogoCreate, name="EstorLogoCreate"),
    path('VisualDetail/<int:pk>/', views.VisualDetail, name="VisualDetail"),
    path('EstorLogoDetail/<int:pk>',views.EstorLogoDetail, name="EstorLogoDetail"),
    path('ItemVisualUpdate/<int:itemId>',views.ItemVisualUpdate, name="ItemVisualUpdate"),
    
   #path('FederationList',views.FederationList, name="FederationList"),
   #path('FederationUpdate/<int:pk>', views.FederationUpdate, name="FederationUpdate")
   #path('FedList', views.FedList, name="FedList"),
    
    

]
