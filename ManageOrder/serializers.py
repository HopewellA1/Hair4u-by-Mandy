from rest_framework import serializers
from .models import Order,OrderItem,PackageItemOrder

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields ='__all__'
  
class OrderItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderItem
		fields ='__all__'
  
class PackageItemOrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = PackageItemOrder
		fields ='__all__'