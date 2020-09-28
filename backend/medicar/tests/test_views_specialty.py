from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from .fixture import SpecialtyFactory

User = get_user_model()


class SpecialtyViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='bruce@user.com', password='foo')
        self.anon_user = User.objects.create_user(email='jane@user.com', password='bar')

        self.unath_client = APIClient()

        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_perform_create(self):
        data = {'name': 'Cardiologia'}
        response = self.unath_client.post(reverse('specialty-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(reverse('specialty-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list(self):
        SpecialtyFactory.create_batch(5)

        response = self.unath_client.get(reverse('specialty-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('specialty-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data), 5)

    def test_retrieve(self):
        specialty = SpecialtyFactory.create(id=10)

        response = self.unath_client.get(reverse('specialty-detail', args=[10]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('specialty-detail', args=[10]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], specialty.name)

    def test_update(self):
        specialty = SpecialtyFactory.create(id=21)
        data = {'name': 'Joe'}
        self.assertNotEqual(specialty.name, data['name'])

        response = self.unath_client.put(reverse('specialty-detail', args=[21]), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(reverse('specialty-detail', args=[21]), data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update(self):
        specialty = SpecialtyFactory.create(id=22)
        data = {'name': 'Joe'}
        self.assertNotEqual(specialty.name, data['name'])

        response = self.unath_client.patch(reverse('specialty-detail', args=[22]), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(reverse('specialty-detail', args=[22]), data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_destroy(self):
        SpecialtyFactory.create(id=15)
        response = self.unath_client.get(reverse('specialty-detail', args=[15]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('specialty-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data), 1)

        response = self.client.delete(reverse('specialty-detail', args=[15]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.get(reverse('specialty-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
