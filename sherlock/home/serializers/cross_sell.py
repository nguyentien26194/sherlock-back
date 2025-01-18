from rest_framework import serializers

from home.models import CrossSellWidget


class CrossSellWidgetSerializer(serializers.ModelSerializer):
    detailed_products = serializers.ReadOnlyField()
    dashboard = serializers.ReadOnlyField()

    class Meta:
        model = CrossSellWidget
        fields = "__all__"
