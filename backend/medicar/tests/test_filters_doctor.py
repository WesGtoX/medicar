from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from .fixture import SpecialtyFactory, DoctorFactory

User = get_user_model()


class DoctorFilterTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='bruce@user.com', password='foo')
        self.anon_user = User.objects.create_user(email='jane@user.com', password='bar')

        self.unath_client = APIClient()

        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        self.specialtyA = SpecialtyFactory.create(name='Cardiologia')
        self.specialtyB = SpecialtyFactory.create(name='Pediatria')
        self.specialtyC = SpecialtyFactory.create(name='Dermatologia')

    def test_filter(self):
        DoctorFactory.create_batch(3, name='Jane', specialty=self.specialtyA)
        DoctorFactory.create_batch(5, name='Bruce', specialty=self.specialtyB)
        DoctorFactory.create_batch(2, name='Alfred', specialty=self.specialtyC)
        DoctorFactory.create_batch(1, name='Jane', specialty=self.specialtyB)

        response = self.client.get(f'{reverse("doctor-list")}{"?search=jane"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        response = self.client.get(f'{reverse("doctor-list")}{"?specialty=1&specialty=3"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        response = self.client.get(f'{reverse("doctor-list")}{"?search=jane&specialty=1&specialty=2"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        response = self.client.get(f'{reverse("doctor-list")}{"?search=Bruce&specialty=1&specialty=3"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
