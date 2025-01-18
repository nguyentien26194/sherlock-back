import json
import logging
from typing import Any

import jwt
from django.apps import apps
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.models import (
    Product,
    Shop,
    UpsellConversion,
    UpsellImpression,
    UpsellWidget,
    Variant,
)
from home.permissions import CheckShopPermission
from home.serializers import (
    ProductSerializer,
    UpsellConversionSerializer,
    UpsellImpressionSerializer,
    UpsellWidgetSerializer,
)
from home.utils import get_object_or_none
from home.views.base import CheckShopModelViewset
from shopify_app.services import ShopifyApiService

logger = logging.getLogger(__file__)


class UpsellWidgetViewSet(CheckShopModelViewset):
    queryset = UpsellWidget.objects.all().order_by("name")
    serializer_class = UpsellWidgetSerializer
    permission_classes = [IsAuthenticated, CheckShopPermission(["shop_id", "shop"])]
    authentication_classes = [JWTAuthentication]

    def retrieve(self, request, pk=None):
        upsell_widget = self.get_object()
        trigger_products = Product.objects.filter(
            cms_product_id__in=upsell_widget.trigger_product_ids
        ).all()
        upsell_widget_data = UpsellWidgetSerializer(upsell_widget).data
        upsell_widget_data["trigger_products"] = ProductSerializer(
            trigger_products, many=True
        ).data

        return Response(upsell_widget_data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_name="extension",
        url_path="extension",
    )
    def extension(self, request: Request, *arg: Any, **kwargs: Any) -> Response:
        shop = get_object_or_none(Shop, shop_url=request.GET.get("shop_url"))
        shopify_service = ShopifyApiService(shop)
        app_response = shopify_service.check_post_purchase_app_in_use()

        if app_response["data"]["app"]["isPostPurchaseAppInUse"]:
            return Response({"app_in_use": True, "shop_url": shop.shop_url})

        return Response({"app_in_use": False, "shop_url": shop.shop_url})

    @action(
        detail=True,
        methods=["put"],
        url_name="update-status",
        url_path="status/update",
    )
    def update_status(self, request: Request, *arg: Any, **kwargs: Any) -> Response:
        upsell_widget = self.get_object()
        upsell_widget.status = request.data.get("status")
        upsell_widget.save()

        return Response(
            {"message": "Upsell widget updated."}, status=status.HTTP_200_OK
        )


class UpsellImpressionViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = UpsellImpressionSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        upsell_widget_id = self.kwargs["id"]
        return UpsellImpression.objects.filter(upsell_widget=upsell_widget_id)

    def perform_create(self, serializer):
        serializer.save(upsell_widget_id=self.kwargs["id"])

    def create(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ):
        data = json.loads(request.body)
        token = data.get("token", None)
        if not token:
            logger.error("Create Upsell Impression: Bad Token.")
            return Response(
                {"message": "Bad Token"}, status=status.HTTP_400_BAD_REQUEST
            )

        decoded_token = jwt.decode(
            token,
            apps.get_app_config("shopify_app").SHOPIFY_API_SECRET_KEY,
            algorithms=["HS256"],
        )
        upsell_impression = get_object_or_none(
            UpsellImpression,
            checkout_token=decoded_token["input_data"]["initialPurchase"][
                "referenceId"
            ],
        )

        if not upsell_impression:
            upsell_widget = UpsellWidget.objects.get(pk=self.kwargs["id"])
            shopify_service = ShopifyApiService(upsell_widget.shop)
            customer_data = shopify_service.get_shopify_customer(
                decoded_token["input_data"]["initialPurchase"]["customerId"]
            )
            UpsellImpression.objects.create(
                upsell_widget=upsell_widget,
                customer_id=decoded_token["input_data"]["initialPurchase"][
                    "customerId"
                ],
                customer_email=customer_data.email,
                customer_first_name=customer_data.first_name,
                customer_last_name=customer_data.last_name,
                cms_product_id=data.get("cms_product_id", ""),
                checkout_token=decoded_token["input_data"]["initialPurchase"][
                    "referenceId"
                ],
            )
            return Response(
                {"message": "Upsell Impression created."},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"message": "Upsell Impression existed."}, status=status.HTTP_200_OK
        )


class UpsellConversionViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = UpsellConversionSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def create(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ):
        data = json.loads(request.body)
        upsell_impression = get_object_or_none(
            UpsellImpression,
            checkout_token=data["referenceId"],
        )
        if not upsell_impression:
            return Response(
                {"message": "Upsell Impression existed."}, status=status.HTTP_200_OK
            )

        variant = get_object_or_none(
            Variant, cms_variant_id=data["changes"][0]["variantId"]
        )
        UpsellConversion.objects.create(
            upsell_impression=upsell_impression,
            variant=variant,
            quantity=data["changes"][0]["quantity"],
        )

        return Response(
            {"message": "Upsell Conversion created."}, status=status.HTTP_201_CREATED
        )
