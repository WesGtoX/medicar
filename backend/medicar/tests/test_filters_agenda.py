from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from faker import Faker

from .fixture import SpecialtyFactory, DoctorFactory, AgendaFactory

User = get_user_model()


class AgendaFilterTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='bruce@user.com', password='foo')
        self.anon_user = User.objects.create_user(email='jane@user.com', password='bar')

        self.unath_client = APIClient()

        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        self.doctorA = DoctorFactory.create(specialty=SpecialtyFactory.create(name='Cardiologia'))
        self.doctorB = DoctorFactory.create(specialty=SpecialtyFactory.create(name='Pediatria'))
        self.doctorC = DoctorFactory.create(specialty=SpecialtyFactory.create(name='Dermatologia'))

    def test_filter(self):
        AgendaFactory.create_batch(
            3, doctor=self.doctorA, day=Faker().date_between(start_date='today', end_date='+10d')
        )
        AgendaFactory.create_batch(
            5, doctor=self.doctorB, day=Faker().date_between(start_date='+20d', end_date='+30d')
        )
        AgendaFactory.create_batch(
            2, doctor=self.doctorC, day=Faker().date_between(start_date='+40d', end_date='+50d')
        )
        AgendaFactory.create_batch(
            1, doctor=self.doctorA, day=Faker().date_between(start_date='+50d', end_date='+60d')
        )

        start_date = Faker().date_between(start_date='+20d', end_date='+20d')
        end_date = Faker().date_between(start_date='+51d', end_date='+51d')

        # filter agenda by one or more doctors
        response = self.client.get(f'{reverse("agenda-list")}{"?doctor=7&doctor=8"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # filter agenda over a range of dates
        response = self.client.get(f'{reverse("agenda-list")}?start_date={start_date}&end_date={end_date}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 7)

        # filter agenda by doctor and specialty
        response = self.client.get(f'{reverse("agenda-list")}{"?doctor=7&specialty=7"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # filter agenda by specialty
        response = self.client.get(f'{reverse("agenda-list")}{"?specialty=7"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # filter without finding data
        response = self.client.get(f'{reverse("agenda-list")}{"?doctor=8&specialty=10&specialty=14"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
