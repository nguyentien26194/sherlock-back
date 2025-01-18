import binascii
import hashlib
import hmac
import logging
import os

import shopify
from django.apps import apps
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import Shop
from home.tasks import create_shop_resources

logger = logging.getLogger(__file__)


def _new_session(shop_url):
    api_key = apps.get_app_config("shopify_app").SHOPIFY_API_KEY
    api_secret_key = apps.get_app_config("shopify_app").SHOPIFY_API_SECRET_KEY
    shopify.Session.setup(api_key=api_key, secret=api_secret_key)
    return shopify.Session(
        shop_url, apps.get_app_config("shopify_app").SHOPIFY_API_VERSION
    )


@api_view(("GET",))
def shopify_login(request):
    if request.GET.get("shop") or request.POST.get("shop"):
        return authenticate(request)

    return Response(
        {"redirect_url": "", "message": "Shop not found."},
        status=status.HTTP_404_NOT_FOUND,
    )


def authenticate(request):
    shop_url = request.GET.get("shop", request.POST.get("shop")).strip()
    scope = apps.get_app_config("shopify_app").SHOPIFY_API_SCOPES
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    redirect_uri = request.build_absolute_uri(reverse("shopify:shopify_app_finalize"))
    permission_url = _new_session(shop_url).create_permission_url(
        scope, redirect_uri, state
    )

    logger.info(f"Authenticate successful", extra={"shop": shop_url})
    return Response({"permission_url": permission_url})


def finalize(request):
    params = request.GET.dict()
    shop_url = params["shop"]
    myhmac = params.pop("hmac")
    line = "&".join([f"{key}={value}" for key, value in sorted(params.items())])
    api_secret_key = apps.get_app_config("shopify_app").SHOPIFY_API_SECRET_KEY
    h = hmac.new(api_secret_key.encode("utf-8"), line.encode("utf-8"), hashlib.sha256)

    if not hmac.compare_digest(h.hexdigest(), myhmac):
        logger.info(
            "Finalize | Could not verify a secure login", extra={"shop": shop_url}
        )
        return redirect(reverse("shopify:shopify_app_login"))

    try:
        shopify_session = _new_session(shop_url)
    except Exception as e:
        logger.error(e.stacktrace())
        return redirect(reverse("shopify:shopify_app_login"))

    access_token = shopify_session.request_token(request.GET)
    create_shop_resources.delay(shop_url, access_token)

    return redirect(
        "{}/{}/?shop_url={}".format(
            apps.get_app_config("home").CLIENT_APP_HOST,
            apps.get_app_config("home").CLIENT_SIGNUP_ROUTE,
            shop_url,
        )
    )
