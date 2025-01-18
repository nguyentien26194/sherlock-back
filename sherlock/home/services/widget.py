from typing import Optional

from django.apps import apps

from home.dataclasses import WidgetContext
from home.models import Shop


class WidgetHTMLService:
    @classmethod
    def widget_context(
        cls, shop: Shop, widget_callback: str, last_name: str
    ) -> Optional[WidgetContext]:
        widget_title = "{}, avant de nous quitter ...".format(last_name)
        widget_description = "On aimerait vous faire découvrir nos produits"

        return WidgetContext(
            widget_callback,
            apps.get_app_config("home").ENVIRONMENT,
            shop.shop_url,
            list(shop.products.all()),
            widget_title,
            widget_description,
        )
