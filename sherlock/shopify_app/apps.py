import os

from django.apps import AppConfig


class ShopifyAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shopify_app"

    SHOPIFY_API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2023-04")

    SHOPIFY_API_SCOPES = [
        "read_discounts",
        "read_orders",
        "read_products",
        "read_script_tags",
        "write_discounts",
        "write_orders",
        "write_script_tags",
        "write_products",
        "read_price_rules",
    ]

    # Shopify Public App Keys
    SHOPIFY_API_KEY = os.environ.get("SHOPIFY_API_KEY")
    SHOPIFY_API_SECRET_KEY = os.environ.get("SHOPIFY_API_SECRET_KEY")

    # --- Script tags ---
    WIDGET_SCRIPT_TAG_SRC = os.environ.get("WIDGET_SCRIPT_TAG_SRC")
    SPLIDE_SCRIPT_TAG_SRC = os.environ.get("SPLIDE_SCRIPT_TAG_SRC")
