import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from home.models import Shop


class ShopFactory(DjangoModelFactory):
    name = factory.Faker("text", max_nb_chars=64)
    email = factory.Faker("email")
    shop_url = factory.Faker("url")
    access_token = factory.Faker("pystr", max_chars=80)
    test = factory.Faker("boolean")

    class Meta:
        model = Shop
        django_get_or_create = ("shop_url",)
