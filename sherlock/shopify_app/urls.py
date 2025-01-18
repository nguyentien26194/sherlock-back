from django.urls import path

from shopify_app import views

app_name = "shopify"

urlpatterns = [
    path("login/", views.shopify_login, name="shopify_app_login"),
    path("authenticate/", views.authenticate, name="shopify_app_authenticate"),
    path("finalize/", views.finalize, name="shopify_app_finalize"),
    path(
        "cross-sell-widget/", views.cross_sell_widget, name="shopify_cross_sell_widget"
    ),
]
