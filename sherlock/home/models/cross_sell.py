from typing import List

from django.contrib.postgres.fields import ArrayField
from django.db import models

from home.models import Widget


class CrossSellWidget(Widget):
    shop = models.ForeignKey("Shop", models.CASCADE, related_name="cross_sell_widgets")
    product_ids = ArrayField(
        base_field=models.CharField(max_length=64), default=list, null=True, blank=True
    )
    selected_all_products = models.BooleanField(default=True)

    class Meta:
        db_table = "cross_sell_widgets"

    @property
    def detailed_products(self) -> List:
        products = (
            self.shop.products.all()[:5]
            if self.selected_all_products
            else self.shop.products.filter(cms_product_id__in=self.product_ids).all()[
                :5
            ]
        )

        return [
            {
                "id": product.id,
                "cms_product_id": product.cms_product_id,
                "title": product.title,
                "shortened_title": product.shortened_title,
                "image_url": product.image_url,
                "description": product.description,
                "price": product.price,
            }
            for product in products
        ]

    @property
    def dashboard(self) -> dict:
        return {
            "impressions": 0,
            "clicks": 0,
            "ctr": 0,
            "sales": 0,
        }
