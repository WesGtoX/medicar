from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from faker import Faker

from .fixture import DoctorFactory, AgendaFactory

User = get_user_model()


class AgendaViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='bruce@user.com', password='foo')
        self.anon_user = User.objects.create_user(email='jane@user.com', password='bar')

        self.unath_client = APIClient()

        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        self.doctor = DoctorFactory.create()

    def test_perform_create(self):
        """register a new agenda"""
        data = {
            'doctor': 1,
            'day': Faker().date_between(start_date='today', end_date='+1y')
        }
        response = self.unath_client.post(reverse('agenda-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(reverse('agenda-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list(self):
        """listing all agendas"""
        AgendaFactory.create_batch(5, doctor=self.doctor)
        AgendaFactory.create_batch(2, doctor=self.doctor)
        AgendaFactory.create_batch(3, doctor=self.doctor, schedule=[])

        response = self.unath_client.get(reverse('agenda-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('agenda-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data), 7)

    def test_retrieve(self):
        """details of a specific agenda"""
        agenda = AgendaFactory.create(id=10)

        response = self.unath_client.get(reverse('agenda-detail', args=[10]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('agenda-detail', args=[10]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['day'], str(agenda.day))
        self.assertIsInstance(response.data['schedule'], list)
        self.assertEqual(response.data.get('doctor')['id'], agenda.doctor.id)
        self.assertEqual(response.data.get('doctor')['name'], agenda.doctor.name)
        self.assertEqual(response.data.get('doctor')['crm'], agenda.doctor.crm)
        self.assertEqual(response.data.get('doctor')['email'], agenda.doctor.email)
        self.assertIsInstance(response.data.get('doctor')['specialty'], dict)

    def test_update(self):
        """methods not allowed returned error 405"""
        AgendaFactory.create(id=15, doctor=self.doctor)
        data = {
            'doctor': 1,
            'day': Faker().date_between(start_date='today', end_date='+0d')
        }

        response = self.unath_client.put(reverse('agenda-detail', args=[21]), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(reverse('agenda-detail', args=[21]), data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update(self):
        """methods not allowed returned error 405"""
        AgendaFactory.create(id=15, doctor=self.doctor)
        data = {
            'doctor': 1,
            'day': Faker().date_between(start_date='today', end_date='+0d')
        }

        response = self.unath_client.patch(reverse('agenda-detail', args=[22]), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(reverse('agenda-detail', args=[22]), data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_destroy(self):
        """methods not allowed returned error 405"""
        AgendaFactory.create(id=15, doctor=self.doctor)
        response = self.unath_client.get(reverse('agenda-detail', args=[15]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('agenda-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data), 1)

        response = self.client.delete(reverse('agenda-detail', args=[15]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.get(reverse('agenda-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
