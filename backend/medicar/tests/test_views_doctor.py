from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from .fixture import DoctorFactory

User = get_user_model()


class DoctorViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='bruce@user.com', password='foo')
        self.anon_user = User.objects.create_user(email='jane@user.com', password='bar')

        self.unath_client = APIClient()

        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_perform_create(self):
        data = {
            'name': 'Jane Joe',
            'crm': 1234,
            'email': 'jane@joe.com',
            'phone': '+55998754128'
        }
        response = self.unath_client.post(reverse('doctor-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(reverse('doctor-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list(self):
        DoctorFactory.create_batch(5)

        response = self.unath_client.get(reverse('doctor-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('doctor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data), 5)

    def test_retrieve(self):
        doctor = DoctorFactory.create(id=10)

        response = self.unath_client.get(reverse('doctor-detail', args=[10]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('doctor-detail', args=[10]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], doctor.name)

    def test_update(self):
        doctor = DoctorFactory.create(id=21)
        data = {'name': 'Joe'}
        self.assertNotEqual(doctor.name, data['name'])

        response = self.unath_client.put(reverse('doctor-detail', args=[21]), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(reverse('doctor-detail', args=[21]), data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update(self):
        doctor = DoctorFactory.create(id=22)
        data = {'name': 'Joe'}
        self.assertNotEqual(doctor.name, data['name'])

        response = self.unath_client.patch(reverse('doctor-detail', args=[22]), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(reverse('doctor-detail', args=[22]), data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_destroy(self):
        DoctorFactory.create(id=15)
        response = self.unath_client.get(reverse('doctor-detail', args=[15]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('doctor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data), 1)

        response = self.client.delete(reverse('doctor-detail', args=[15]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.get(reverse('doctor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
