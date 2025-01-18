from __future__ import annotations

from dataclasses import dataclass
from typing import List

from home.models import Product


@dataclass
class WidgetContext:
    widget_callback: str
    environment: str
    shop_url: str
    products: List[Product]
    widget_title: str
    widget_description: str
