from rest_framework import serializers

from home.models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        exclude = ("access_token",)
