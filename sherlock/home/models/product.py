from decimal import Decimal

from django.contrib.postgres.fields import ArrayField
from django.db import models

from home.models import TimeStampMixin


class Product(TimeStampMixin):
    shop = models.ForeignKey("Shop", models.CASCADE, related_name="products")
    title = models.TextField(null=True)
    image_url = models.URLField(max_length=1000, null=True)
    image_urls = ArrayField(
        base_field=models.URLField(max_length=1000, null=True), null=True
    )
    cms_product_id = models.CharField(max_length=20, unique=True)
    cms_product_handle = models.TextField(null=True)
    variant_options = ArrayField(base_field=models.JSONField(), null=True)
    description = models.TextField(null=True)

    class Meta:
        db_table = "products"

    @property
    def price(self) -> str:
        variants = self.variants.all()
        return variants[0].price if variants else ""

    @property
    def visit_url(self) -> str:
        return "https://{}/products/{}".format(
            self.shop.shop_url, self.cms_product_handle
        )

    @property
    def shortened_title(self, max_length: int = 40) -> str:
        if len(self.title) > max_length:
            return self.title[:40] + "..."
        return self.title


class Variant(TimeStampMixin):
    shop_url = models.URLField()
    image_url = models.URLField(max_length=1000, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.TextField(null=True)
    options = ArrayField(base_field=models.CharField(max_length=1000, null=True))
    inventory_quantity = models.IntegerField(default=0)
    product = models.ForeignKey("Product", models.CASCADE, related_name="variants")
    cms_variant_id = models.CharField(max_length=20)

    class Meta:
        db_table = "variants"
