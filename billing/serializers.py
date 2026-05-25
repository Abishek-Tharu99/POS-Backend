from rest_framework import serializers
from .models import Item,Bill,BillItem,Payment

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'