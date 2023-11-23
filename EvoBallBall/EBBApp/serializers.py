from rest_framework import serializers
from .models import Buyer, Product, Category, Order


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ('name', 'surname', 'email', 'delivery_information')


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'size', 'price')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'