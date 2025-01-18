from __future__ import annotations

from typing import Any, List

from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class CheckShopPermission(BasePermission):
    """
    Custom permission that checks whether current user is assinged to the shop
    with id `shop_id`
    """

    def __init__(self, shop_field_names: List[str] = ["shop"]) -> None:
        self.shop_field_names = shop_field_names
        super().__init__()

    def __call__(self, *args: Any, **kwargs: Any) -> CheckShopPermission:
        return self

    def has_permission(self, request: Request, view) -> bool:
        if not request.user.shop:
            return False

        user_shop_id = request.user.shop.id
        for field_name in self.shop_field_names:
            shop_id = None
            if field_name in request.data:
                shop_id = request.data[field_name]
            if field_name in request.query_params:
                shop_id = request.query_params[field_name]

            # Try to convert shop_id to int and check if it is present in user shop ids
            # If it's shop_id is not convertable to int, return False
            try:
                if shop_id and int(shop_id) != user_shop_id:
                    return False
            except ValueError:
                return False

        return super().has_permission(request, view)
