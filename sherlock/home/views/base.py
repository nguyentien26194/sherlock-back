from typing import Optional

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response


class CheckShopModelViewset(viewsets.ModelViewSet):
    """
    Custom ModelViewset that requires an additional parameter with shop id.
    Checks whether current user is assinged to this shop.
    """

    shop_field_name = "shop"

    @staticmethod
    def check_shop_id(
        request: Request, shop_id: Optional[int] = None
    ) -> Optional[Response]:
        """
        Check whether `shop_id` query parameter was specified.
        Ensure that current user has a shop with this id.
        """
        if not shop_id:
            shop_id_str = request.GET.get("shop_id", None)
            if shop_id_str:
                shop_id = int(shop_id_str)
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"shop_id": "Shop id is a required query parameter"},
                )

        if hasattr(request.user, "shop"):
            user_shop_id = request.user.shop.id
        else:
            user_shop_id = None

        if int(shop_id) != user_shop_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def list(self, request: Request, *args, **kwargs) -> Response:
        shop_id = int(request.GET.get("shop_id", None))
        queryset = self.filter_queryset(self.get_queryset()).filter(
            **{f"{self.shop_field_name}__id": shop_id}
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()

        shop = getattr(instance, self.shop_field_name)
        response = self.check_shop_id(request, shop.id)
        if response:
            return response

        return super().retrieve(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shop_id = serializer.validated_data[self.shop_field_name].id
        response = self.check_shop_id(request, shop_id)
        if response:
            return response

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()

        shop = getattr(instance, self.shop_field_name)
        response = self.check_shop_id(request, shop.id)
        if response:
            return response

        return super().update(request, *args, **kwargs)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()

        shop = getattr(instance, self.shop_field_name)
        response = self.check_shop_id(request, shop.id)
        if response:
            return response

        return super().destroy(request, *args, **kwargs)
