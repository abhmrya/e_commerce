from rest_framework import serializers
from .models import Product, Backgroundimg, Specialproduct, Cart, CartItem, Profile

class BackgroundimgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backgroundimg
        fields = '__all__'

class SpecialproductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialproduct
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, source='cartitem_set')
    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'cart_items']
