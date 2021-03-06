from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from .fixture import SpecialtyFactory

User = get_user_model()


class SpecialtyFilterTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='bruce@user.com', password='foo')
        self.anon_user = User.objects.create_user(email='jane@user.com', password='bar')

        self.unath_client = APIClient()

        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_filter(self):
        SpecialtyFactory.create_batch(3, name='Cardiologia')
        SpecialtyFactory.create_batch(5, name='Pediatria')

        # filter specialty by name
        response = self.client.get(f'{reverse("specialty-list")}{"?search=Cardiologia"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        # filter specialty by containing in your name
        response = self.client.get(f'{reverse("specialty-list")}{"?search=ped"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        # filter without finding data
        response = self.client.get(f'{reverse("specialty-list")}{"?search=pat"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
