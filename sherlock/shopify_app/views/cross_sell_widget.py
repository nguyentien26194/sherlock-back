import logging

from django.http import HttpResponse
from django.template import Context, Template
from rest_framework.decorators import api_view
from rest_framework.request import Request

from home.models import Shop
from home.services.widget import WidgetHTMLService
from home.templates.widget import CROSS_SELL_WIDGET_HTML_TEMPLATE
from home.utils import asdict_with_properties, get_object_or_none

logger = logging.getLogger(__file__)


@api_view(("GET",))
def cross_sell_widget(request: Request) -> HttpResponse:
    content_type = "application/javascript"
    shop_url = request.GET.get("shop")
    email = request.GET.get("checkout_customer_email", "")
    last_name = request.GET.get("checkout_shipping_address_last_name", "")
    widget_callback = request.GET.get("jsonp")

    shop = get_object_or_none(Shop, shop_url=shop_url)
    context = WidgetHTMLService.widget_context(shop, widget_callback, last_name)
    if not context:
        return HttpResponse(b"", content_type=content_type)

    template = Template(CROSS_SELL_WIDGET_HTML_TEMPLATE)
    widget_text = template.render(Context(asdict_with_properties(context)))
    return HttpResponse(widget_text, content_type=content_type)
