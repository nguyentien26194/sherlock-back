from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.models import Discount, DiscountType, Shop
from home.serializers import DiscountSerializer
from home.utils import get_object_or_none
from home.views.base import CheckShopModelViewset


class DiscountViewSet(CheckShopModelViewset):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        shop = get_object_or_none(Shop, id=data[self.shop_field_name].id)
        if not shop:
            return Response(
                {"message": "Shop not found."}, status=status.HTTP_404_NOT_FOUND
            )

        discount_value = float(data["value"]) * (
            0.01 if data["value_type"] == DiscountType.PERCENTAGE.value else 1
        )

        # cms_discount_result = create_cms_discount(
        #     shop.id,
        #     data["code"] if "code" in data else "",
        #     data["value_type"],
        #     discount_value,
        #     data["start_date"].isoformat(),
        #     data["end_date"].isoformat() if data["end_date"] else None,
        # )

        # if "error" in cms_discount_result:
        #     return Response({"error": cms_discount_result["error"]}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)
