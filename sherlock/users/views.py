from typing import Any

from django.conf import settings
from django.contrib.auth.hashers import check_password
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from home.models import Shop
from home.utils import get_object_or_none
from users.models import User
from users.serializers import (
    CookieTokenRefreshSerializer,
    LoginSerializer,
    SignUpSerializer,
    UserSerializer,
)


class UserViewset(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=["post"],
        url_name="signup",
        url_path="signup",
        permission_classes=[AllowAny],
    )
    def signup_user(self, request: Request, *args, **kwargs) -> Response:
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shop = get_object_or_none(Shop, shop_url=serializer.data["shop_url"])
        if not shop:
            return Response(
                {"message": "Shop not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user, _ = User.objects.update_or_create(
            email=serializer.data["email"],
            defaults={
                "first_name": serializer.data["first_name"],
                "last_name": serializer.data["last_name"],
            },
        )
        user.shop = shop
        user.set_password(serializer.data["password"])
        user.is_active = True
        user.save()

        # if apps.get_app_config("home").is_production():
        #     send_new_shop_email.delay(
        #         shop.shop_url,
        #         serializer.data["email"],
        #         serializer.data["first_name"],
        #         serializer.data["last_name"],
        #     )

        # if not user.is_active:
        #     activation_token = User.generate_activation_token(user.email)
        #     send_email_activation_email.delay(
        #         user.id, serializer.data["email"], serializer.data["first_name"], activation_token
        #     )

        return Response({"message": "User created."}, status=status.HTTP_200_OK)


@api_view(("POST",))
def obtain_token_pairs(request: Request) -> Response:
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data["email"]
    password = serializer.data["password"]
    user = get_object_or_none(User, email=email)

    if not user:
        return Response(
            {"message": "Email not found."}, status=status.HTTP_404_NOT_FOUND
        )

    if not check_password(password, user.password):
        return Response(
            {"message": "Wrong password."}, status=status.HTTP_404_NOT_FOUND
        )

    if not user.is_active:
        return Response(
            {"message": "User is not active."}, status=status.HTTP_404_NOT_FOUND
        )

    refresh = RefreshToken.for_user(user)
    response = Response()
    response.data = {
        "access": str(refresh.access_token),
        "shop_id": user.shop.id,
        "shop_url": user.shop.shop_url,
        "shop_name": user.shop.name,
        "logo_url": user.shop.logo_url,
    }
    response.set_cookie(
        "refresh",
        str(refresh),
        max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
        httponly=True,
    )

    return response


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(
        self, request: Request, response: Response, *args: Any, **kwargs: Any
    ) -> Response:
        if response.data.get("refresh"):
            response.set_cookie(
                "refresh",
                response.data["refresh"],
                max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                httponly=True,
            )
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)
