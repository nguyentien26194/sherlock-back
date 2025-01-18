from decimal import Decimal

from django.db import models

from home.models import TimeStampMixin


class DiscountType(models.TextChoices):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"


class DiscountStatus(models.TextChoices):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"
    EXPIRED = "expired"
    SCHEDULED = "scheduled"


class Discount(TimeStampMixin):
    shop = models.ForeignKey("Shop", models.CASCADE, related_name="discounts")
    code = models.CharField(max_length=20, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    value_type = models.CharField(choices=DiscountType.choices, max_length=12)
    status = models.CharField(choices=DiscountStatus.choices, max_length=12)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    cmd_discount_id = models.CharField(max_length=64, null=True)

    class Meta:
        db_table = "discounts"

    def symbol(self) -> str:
        return "%" if self.value_type == DiscountType.PERCENTAGE.value else "€"

    def standard_value(self) -> str:
        return (
            str(self.value.to_integral())
            if self.value == self.value.to_integral()
            else str(self.value.normalize())
        )
