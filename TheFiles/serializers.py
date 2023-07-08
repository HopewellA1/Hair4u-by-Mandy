from rest_framework import serializers
from .models import ItemVisual, EstorLogo

class ItemVisualSerializer(serializers.ModelSerializer):
	class Meta:
		model = ItemVisual
		fields ='__all__'
  
class EstorLogoSerializer(serializers.ModelSerializer):
	class Meta:
		model = EstorLogo
		fields ='__all__'