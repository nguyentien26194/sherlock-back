from factory.django import DjangoModelFactory

from faker import Faker

fake = Faker("fr_FR")

from home.models import Shop


class ShopFactory(DjangoModelFactory):
    name = fake.text(max_nb_chars=64)
    email = fake.email()
    shop_url = fake.url()
    access_token = fake.pystr()
    test = fake.boolean()

    class Meta:
        model = Shop
        django_get_or_create = ("shop_url",)
