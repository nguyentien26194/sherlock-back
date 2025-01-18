import os

from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"

    # --- General ---
    APP_HOST = os.environ.get("APP_HOST")
    CLIENT_APP_HOST = os.environ.get("CLIENT_APP_HOST")
    ENVIRONMENT = os.environ.get("ENVIRONMENT")
    CLIENT_LOGIN_ROUTE = "login"
    CLIENT_SIGNUP_ROUTE = "signup"

    # --- Security ---
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # --- AWS ---
    AWS_REGION = os.environ.get("AWS_REGION")
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
