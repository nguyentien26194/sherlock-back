from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.models import CrossSellWidget, Shop, WidgetStatus
from home.permissions import CheckShopPermission
from home.serializers import CrossSellWidgetSerializer
from home.views.base import CheckShopModelViewset


class CrossSellWidgetViewSet(CheckShopModelViewset):
    queryset = CrossSellWidget.objects.all().order_by("name")
    serializer_class = CrossSellWidgetSerializer
    permission_classes = [IsAuthenticated, CheckShopPermission(["shop_id", "shop"])]
    authentication_classes = [JWTAuthentication]
