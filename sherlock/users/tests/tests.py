from django.urls import reverse
from rest_framework.test import APITestCase

from home.tests.factories import ShopFactory
from users.tests.factories import UserFactory


class UserAuthTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = UserFactory.create(is_active=True)
        cls.shop = ShopFactory.create()
        cls.user_data = {"email": cls.user.email, "password": cls.user.password}
        cls.user.set_password(cls.user.password)
        cls.user.shop = cls.shop
        cls.user.save()

    def test_obtain_token_pairs(self):
        response = self.client.post(reverse("users:auth_token"), data=self.user_data)
        self.assertEqual(
            response.status_code, 200, "User should be able to obtain auth token"
        )

        response = self.client.post(reverse("users:auth_token_refresh"))
        self.assertEqual(
            response.status_code, 200, "User should be able to refresh auth token"
        )
