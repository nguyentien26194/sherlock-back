from home.celery import app
from home.models import Product, Shop, Variant
from shopify_app.services import ShopifyApiService


@app.task
def save_cms_products(shop_id: int) -> None:
    shop = Shop.objects.get(pk=shop_id)

    shopify_service = ShopifyApiService(shop)
    cms_products = shopify_service.get_shopify_products()

    saved_product_ids = []
    for cms_product in cms_products:
        if cms_product.images:
            cms_variants = cms_product.variants
            saved_product_ids.append(cms_product.id)
            product, _ = Product.objects.update_or_create(
                shop=shop,
                cms_product_id=cms_product.id,
                defaults={
                    "title": cms_product.title,
                    "description": cms_product.body_html,
                    "cms_product_handle": cms_product.handle,
                    "image_urls": [i.src for i in cms_product.images],
                    "image_url": cms_product.images[0].src
                    if cms_product.images
                    else "",
                    "variant_options": [
                        {"name": option.name, "values": option.values}
                        for option in cms_product.options
                    ],
                },
            )

            saved_variant_ids = []
            for cms_variant in cms_variants:
                saved_variant_ids.append(cms_variant.id)
                image = [
                    img for img in cms_product.images if img.id == cms_variant.image_id
                ]
                variant, _ = Variant.objects.update_or_create(
                    shop_url=shop.shop_url,
                    product=product,
                    cms_variant_id=cms_variant.id,
                    defaults={
                        "image_url": image[0].src if len(image) > 0 else None,
                        "price": cms_variant.price,
                        "title": cms_variant.title,
                        "options": [
                            cms_variant.option1,
                            cms_variant.option2,
                            cms_variant.option3,
                        ],
                        "inventory_quantity": cms_variant.inventory_quantity,
                    },
                )

            Variant.objects.filter(shop_url=shop.shop_url, product=product).exclude(
                cms_variant_id__in=saved_variant_ids
            ).delete()

    Product.objects.filter(shop=shop).exclude(
        cms_product_id__in=saved_product_ids
    ).delete()
