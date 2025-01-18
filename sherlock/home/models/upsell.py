from decimal import Decimal

from django.contrib.postgres.fields import ArrayField
from django.db import models

from home.models import DiscountType, Product, TimeStampMixin, Widget


class UpsellWidget(Widget):
    shop = models.ForeignKey("Shop", models.CASCADE, related_name="upsell_widgets")
    offer_name = models.CharField(max_length=256, null=True)
    offer_description = models.TextField(null=True)
    upsell_product_id = models.CharField(max_length=64)
    minimum_amount_requirements = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    minimum_quantity_requirements = models.IntegerField(null=True)
    trigger_product_ids = ArrayField(
        base_field=models.CharField(max_length=64), default=list, null=True, blank=True
    )
    selected_all_trigger_products = models.BooleanField(default=True)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_value_type = models.CharField(
        choices=DiscountType.choices, max_length=12, null=True
    )

    class Meta:
        db_table = "upsell_widgets"

    @property
    def detailed_product(self) -> dict:
        product = Product.objects.get(
            shop=self.shop, cms_product_id=self.upsell_product_id
        )
        return {
            "id": product.id,
            "cms_product_id": product.cms_product_id,
            "title": product.title,
            "image_url": product.image_url,
            "image_urls": product.image_urls,
            "description": product.description,
            "price": product.price,
        }

    @property
    def detailed_variants(self) -> dict:
        product = Product.objects.get(
            shop=self.shop, cms_product_id=self.upsell_product_id
        )
        variants = product.variants.all()
        return [
            {
                "cms_variant_id": variant.cms_variant_id,
                "title": variant.title,
                "price": variant.price,
                "image_url": variant.image_url,
                "options": variant.options,
            }
            for variant in variants
        ]

    @property
    def dashboard(self) -> dict:
        impressions = self.upsell_impressions.all()
        clicks = 0
        sales = 0
        sales_count = 0
        for impression in impressions:
            upsell_conversion = (
                impression.upsell_conversion
                if hasattr(impression, "upsell_conversion")
                else None
            )
            if upsell_conversion:
                clicks += 1
                sales += upsell_conversion.sales
                sales_count += 1
        ctr = clicks / impressions.count() if impressions else 0
        return {
            "impressions": impressions.count(),
            "clicks": clicks,
            "ctr": round(ctr * 100, 2),
            "sales": sales,
        }


class UpsellImpression(TimeStampMixin):
    upsell_widget = models.ForeignKey(
        "UpsellWidget", models.CASCADE, related_name="upsell_impressions"
    )
    cms_product_id = models.CharField(max_length=64)
    checkout_token = models.CharField(max_length=256, null=True)
    customer_id = models.CharField(max_length=256, null=True)
    customer_email = models.EmailField(null=True)
    customer_first_name = models.CharField(max_length=128, null=True)
    customer_last_name = models.CharField(max_length=128, null=True)

    class Meta:
        db_table = "upsell_impressions"


class UpsellConversion(TimeStampMixin):
    upsell_impression = models.OneToOneField(
        UpsellImpression, models.CASCADE, related_name="upsell_conversion"
    )
    variant = models.ForeignKey(
        "Variant", models.CASCADE, related_name="upsell_conversions"
    )
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = "upsell_conversions"

    @property
    def sales(self):
        discount_value = self.upsell_impression.upsell_widget.discount_value
        discount_value_type = self.upsell_impression.upsell_widget.discount_value_type
        if discount_value_type == "percentage":
            discounted_price = self.variant.price * (
                Decimal(1) - discount_value / Decimal(100)
            )
        else:
            discounted_price = abs(self.variant.price - discount_value)
        return self.quantity * discounted_price
