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
        self.specialtyA = SpecialtyFactory.create(id=21, name='Cardiologia')
        self.specialtyB = SpecialtyFactory.create(id=22, name='Pediatria')
        self.specialtyC = SpecialtyFactory.create(id=23, name='Dermatologia')

    def test_filter(self):
        DoctorFactory.create_batch(3, name='Jane', specialty=self.specialtyA)
        DoctorFactory.create_batch(5, name='Bruce', specialty=self.specialtyB)
        DoctorFactory.create_batch(2, name='Alfred', specialty=self.specialtyC)
        DoctorFactory.create_batch(1, name='Jane', specialty=self.specialtyB)

        # filter médicos by name
        response = self.client.get(f'{reverse("doctor-list")}{"?search=jane"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        # filter doctors by name and specialty
        response = self.client.get(f'{reverse("doctor-list")}{"?specialty=21&specialty=23"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        # filter doctors by name and by one or more specialty
        response = self.client.get(f'{reverse("doctor-list")}{"?search=jane&specialty=21&specialty=22"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        # filter without finding data
        response = self.client.get(f'{reverse("doctor-list")}{"?search=Bruce&specialty=21&specialty=23"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
