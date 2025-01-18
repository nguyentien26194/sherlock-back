from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from home.views import (
    CrossSellWidgetViewSet,
    DiscountViewSet,
    ProductViewSet,
    UpsellWidgetViewSet,
    health,
)

router = routers.DefaultRouter()
router.register(r"upsell-widgets", UpsellWidgetViewSet, basename="upsell-widgets")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"discounts", DiscountViewSet, basename="discounts")
router.register(
    r"cross-sell-widgets", CrossSellWidgetViewSet, basename="cross-sell-widgets"
)

urlpatterns = [
    path("", include(router.urls)),
    path("health", health),
]
