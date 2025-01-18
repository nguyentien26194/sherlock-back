from home.celery import app
from home.models import Shop
from home.tasks.product import save_cms_products
from shopify_app.services import ShopifyApiService


@app.task
def create_shop_resources(shop_url: str, access_token: str) -> None:
    shop, _ = Shop.objects.update_or_create(
        shop_url=shop_url,
        defaults={
            "access_token": access_token,
        },
    )

    shopify_service = ShopifyApiService(shop)
    current_shop = shopify_service.get_current_shop()
    shop.name = current_shop.name
    shop.email = current_shop.email
    shop.save()
    shopify_service.create_script_tags()
    save_cms_products.delay(shop.id)
