from pathlib import PurePosixPath

from django.apps import apps
from django.db import models

from home.models import CMS, TimeStampMixin


class Shop(TimeStampMixin):
    name = models.CharField(max_length=128)
    email = models.EmailField(null=True)
    shop_url = models.URLField(unique=True)
    access_token = models.CharField(max_length=80)
    test = models.BooleanField(default=False)
    logo_uploaded = models.BooleanField(default=False)
    logo_extension = models.CharField(max_length=8, null=True)
    trial_ends_on = models.DateTimeField(null=True)
    cms = models.CharField(
        choices=CMS.choices, max_length=16, default=CMS.SHOPIFY.value
    )

    class Meta:
        db_table = "shops"

    def __str__(self) -> str:
        return "{}: {}".format(self.name, str(self.shop_url))

    @property
    def logo_url(self) -> str:
        if self.logo_uploaded:
            return "https://{}.s3.{}.amazonaws.com/logos/[{}]{}_logo.{}".format(
                apps.get_app_config("home").S3_BUCKET_NAME,
                apps.get_app_config("home").AWS_REGION,
                self.id,
                self.shop_url,
                self.logo_extension if self.logo_extension else "png",
            )

        return "{}/logos/{}.svg".format(
            apps.get_app_config("home").CLIENT_APP_HOST,
            self.name[0].lower().replace("é", "e"),
        )

    @property
    def logo_filepath(self) -> PurePosixPath:
        return PurePosixPath(
            "logos/[{id}]{url}_logo.{extension}".format(
                id=self.id,
                url=self.shop_url,
                extension=self.logo_extension if self.logo_extension else "png",
            )
        )
