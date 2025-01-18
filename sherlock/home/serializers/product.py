from rest_framework import serializers

from home.models import Product


class ProductSerializer(serializers.ModelSerializer):
    shortened_title = serializers.ReadOnlyField()
    price = serializers.ReadOnlyField()
    inventory_quantity = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = "__all__"
