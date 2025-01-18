from rest_framework import serializers

from home.models import UpsellConversion, UpsellImpression, UpsellWidget


class UpsellWidgetSerializer(serializers.ModelSerializer):
    detailed_product = serializers.ReadOnlyField()
    dashboard = serializers.ReadOnlyField()

    class Meta:
        model = UpsellWidget
        fields = "__all__"


class UpsellWidgetOfferSerializer(serializers.ModelSerializer):
    detailed_product = serializers.ReadOnlyField()
    detailed_variants = serializers.ReadOnlyField()

    class Meta:
        model = UpsellWidget
        fields = (
            "id",
            "offer_name",
            "offer_description",
            "detailed_product",
            "detailed_variants",
            "discount_value",
            "discount_value_type",
        )


class UpsellImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpsellImpression
        exclude = ["upsell_widget"]


class UpsellConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpsellConversion
        exclude = ["upsell_impression"]
