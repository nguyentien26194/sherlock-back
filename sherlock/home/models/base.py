from django.db import models


class CMS(models.TextChoices):
    SHOPIFY = "Shopfiy"
    PRESTA = "Presta"


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class DiscountType(models.TextChoices):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"


class WidgetStatus(models.TextChoices):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"


class Widget(TimeStampMixin):
    name = models.CharField(max_length=128, null=True)
    description = models.TextField(null=True)
    status = models.CharField(
        choices=WidgetStatus.choices, max_length=12, default=WidgetStatus.ACTIVE.value
    )

    class Meta:
        abstract = True
