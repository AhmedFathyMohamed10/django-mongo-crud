from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    unit_price = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'product_id', 'username', 'product_name', 'unit_price', 'quantity', 'total_cost', 'order_date']
        
    def get_product_name(self, obj):
        return obj.product_id.name if obj.product_id else None
    
    def get_unit_price(self, obj):
        return obj.product_id.price if obj.product_id else None
    
    def get_username(self, obj):
        return obj.user.username if obj.user else None
    

class CartSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'username', 'order', 'total_cost']

    def get_username(self, obj):
        return obj.user.username if obj.user else None 
    
    def get_total_cost(self, obj):
        return obj.get_total_cost() if hasattr(obj, 'get_total_cost') else None