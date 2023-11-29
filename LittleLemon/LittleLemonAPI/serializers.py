from rest_framework import serializers
from .models import MenuItem
from .models import Category
from decimal import Decimal
import bleach


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    # to run a method
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = "__all__"

        """
        extra_kwargs = {
            "price": {"min_value": 2},
        }
        """

    """
    def validate_price(self, value):
        if value < 2:
            raise serializers.ValidationError("price should not be less than 2")
    def validate_title(self,value):
        return bleach.clean(value)
    """
