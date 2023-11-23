from rest_framework import serializers
from .models import MenuItem
from .models import Category
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    # to change the name
    stock = serializers.IntegerField(source="inventory")
    # to run a method
    price_after_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    #category = CategorySerializer()
    category = serializers.HyperlinkedRelatedField(
        queryset = Category.objects.all(),
        view_name='category-detail'
    )
    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "stock", "price_after_tax"]

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)
