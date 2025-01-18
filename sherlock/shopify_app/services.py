import json
import logging
from typing import Dict

import shopify
from django.apps import apps

from home.models import Shop

logger = logging.getLogger(__name__)


class ShopifyApiService:
    api_version = apps.get_app_config("shopify_app").SHOPIFY_API_VERSION
    api_key = apps.get_app_config("shopify_app").SHOPIFY_API_KEY
    api_secret_key = apps.get_app_config("shopify_app").SHOPIFY_API_SECRET_KEY

    def __init__(self, shop: Shop) -> None:
        self.shop = shop
        self.shopify = shopify

    def _connect_shopify(self):
        shopify.Session.setup(api_key=self.api_key, secret=self.api_secret_key)
        shopify_session = shopify.Session(self.shop.shop_url, self.api_version)
        shopify_session.token = self.shop.access_token
        shopify.ShopifyResource.activate_session(shopify_session)

    def _disconnect_shopify(self):
        shopify.ShopifyResource.clear_session()

    def _create_script_tag(self, src: str):
        query = """
            mutation scriptTagCreate($input: ScriptTagInput!) {
                scriptTagCreate(input: $input) {
                    scriptTag {
                        id
                        src
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }
            """
        return json.loads(
            shopify.GraphQL().execute(
                query=query,
                variables={
                    "input": {
                        "cache": False,
                        "displayScope": "ORDER_STATUS",
                        "src": src,
                    }
                },
            )
        )

    def get_current_shop(self) -> shopify.Shop:
        self._connect_shopify()
        current_shop = self.shopify.Shop.current()
        self._disconnect_shopify()
        return current_shop

    def get_shopify_products(self) -> list:
        self._connect_shopify()
        page_count = 0
        products_count = shopify.Product.count(status="active")
        shopify_products = []
        if products_count > 0:
            page = shopify.Product.find(limit=250, status="active")
            shopify_products.extend(page)
            while page.has_next_page():
                page = page.next_page()
                shopify_products.extend(page)
                page_count += 1

        self._disconnect_shopify()
        return shopify_products

    def create_script_tags(self):
        script_tags_srcs = [
            apps.get_app_config("shopify_app").WIDGET_SCRIPT_TAG_SRC,
            apps.get_app_config("shopify_app").SPLIDE_SCRIPT_TAG_SRC,
        ]

        self._connect_shopify()

        existing_script_tags = shopify.ScriptTag.find()
        if existing_script_tags:
            for script_tag in existing_script_tags:
                shopify.ScriptTag.delete(script_tag.id)

        for src in script_tags_srcs:
            script_tag_response = self._create_script_tag(src)
            if script_tag_response["data"]["scriptTagCreate"]["userErrors"]:
                logger.error(
                    "{}: Error when creating script tag - {}: {}".format(
                        self.shop.shop_url,
                        src,
                        script_tag_response["data"]["scriptTagCreate"]["userErrors"][0][
                            "message"
                        ],
                    )
                )

        self._disconnect_shopify()
