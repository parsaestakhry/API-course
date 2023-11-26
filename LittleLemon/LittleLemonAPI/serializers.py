from rest_framework import serializers
from .models import MenuItem
from .models import Category
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    # to run a method
    price_after_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = "__all__"

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)
