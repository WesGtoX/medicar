from datetime import datetime, timedelta
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from faker import Faker

from .fixture import DoctorFactory, AgendaFactory, MedicalAppointmentFactory

User = get_user_model()


class MedicalAppointmentViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='bruce@user.com', password='foo')
        self.anon_user = User.objects.create_user(email='jane@user.com', password='bar')

        self.unath_client = APIClient()

        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        self.doctor = DoctorFactory.create()
        self.agenda = AgendaFactory.create(id=1, doctor=self.doctor)
        self.past = AgendaFactory.create(id=17, doctor=self.doctor, day='2010-01-01')

    def test_perform_create(self):
        """create a medical appointment"""
        data = {'agenda_id': 1, 'hourly': '09:00'}
        response = self.unath_client.post(reverse('medicalappointment-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(reverse('medicalappointment-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {'agenda_id': 1, 'hourly': ''}
        response = self.client.post(reverse('medicalappointment-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('formato inválido', response.data.get('error')['message'])

        data = {'agenda_id': 17, 'hourly': '09:00'}
        response = self.client.post(reverse('medicalappointment-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tempo passado', response.data.get('error')['message'])

    def test_list(self):
        """list medical appointments"""
        past_time = (datetime.now() - timedelta(hours=0.04)).strftime('%H:%M')
        agenda1 = AgendaFactory.create(id=101, day='2019-01-01')
        agenda2 = AgendaFactory.create(id=102, day=Faker().date_between(start_date='+6d', end_date='+1y'))
        agenda3 = AgendaFactory.create(id=103, day=Faker().date_between(start_date='+9d', end_date='+1y'))
        agenda4 = AgendaFactory.create(id=104, day=Faker().date_between(start_date='+0d', end_date='+1d'))
        MedicalAppointmentFactory.create(id=101, agenda=agenda1, patient=self.user)
        MedicalAppointmentFactory.create(id=102, agenda=agenda2, patient=self.user)
        MedicalAppointmentFactory.create(id=103, agenda=agenda3, patient=self.user)
        MedicalAppointmentFactory.create(id=104, agenda=agenda4, hourly=past_time, patient=self.user)

        response = self.unath_client.get(reverse('medicalappointment-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('medicalappointment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data), 2)

    def test_retrieve(self):
        """methods not allowed returned error 405"""
        MedicalAppointmentFactory.create(id=10, agenda=self.agenda, hourly='09:00', patient=self.user)

        response = self.unath_client.get(reverse('medicalappointment-detail', args=[10]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('medicalappointment-detail', args=[10]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update(self):
        """methods not allowed returned error 405"""
        MedicalAppointmentFactory.create(id=21, agenda=self.agenda, hourly='09:00', patient=self.user)
        data = {'hourly': '10:00'}

        response = self.unath_client.put(reverse('medicalappointment-detail', args=[21]), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(reverse('medicalappointment-detail', args=[21]), data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update(self):
        """methods not allowed returned error 405"""
        MedicalAppointmentFactory.create(id=22, agenda=self.agenda, hourly='09:00', patient=self.user)
        data = {'hourly': '10:00'}

        response = self.unath_client.patch(reverse('medicalappointment-detail', args=[22]), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(reverse('medicalappointment-detail', args=[22]), data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_destroy(self):
        """remove medical appointments"""
        MedicalAppointmentFactory.create(id=15, agenda=self.agenda, hourly='09:00', patient=self.user)
        MedicalAppointmentFactory.create(id=16, agenda=self.past, hourly='08:00', patient=self.user)

        response = self.unath_client.get(reverse('medicalappointment-detail', args=[15]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('medicalappointment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data), 2)

        response = self.client.delete(reverse('medicalappointment-detail', args=[15]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(reverse('medicalappointment-detail', args=[16]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('já foi realizada', response.data.get('error')['message'])

        response = self.client.get(reverse('medicalappointment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
