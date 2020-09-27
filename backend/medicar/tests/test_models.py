import datetime
from faker import Faker

from django.contrib.auth import get_user_model
from django.test import TestCase

from medicar.models import (
    Specialty, Doctor, Agenda, MedicalAppointment
)


class SpecialtyModelTestCase(TestCase):

    def test_create_specialty(self):
        specialty = Specialty.objects.create(name='Cardiologia')
        self.assertEqual(specialty.name, 'Cardiologia')
        self.assertEqual(str(specialty), 'Cardiologia')


class DoctorModelTestCase(TestCase):

    def setUp(self):
        self.specialty = Specialty.objects.create(name='Cardiologia')

    def test_create_doctor(self):
        doctor = Doctor.objects.create(
            name='Bruce',
            crm=1234,
            email='bruce@wayne.com',
            phone='+5516991237654',
            specialty=self.specialty
        )
        self.assertEqual(doctor.name, 'Bruce')
        self.assertEqual(doctor.crm, 1234)
        self.assertEqual(doctor.email, 'bruce@wayne.com')
        self.assertEqual(doctor.phone, '+5516991237654')
        self.assertEqual(str(doctor.specialty), self.specialty.name)
        self.assertEqual(str(doctor), 'Bruce')


class AgendaModelTestCase(TestCase):

    def setUp(self):
        specialty = Specialty.objects.create(name='Pediatria')
        self.doctor = Doctor.objects.create(
            name='Jane',
            crm=4567,
            email='jane@joe.com',
            phone='+5516992457046',
            specialty=specialty
        )

    def test_create_agenda(self):
        agenda = Agenda.objects.create(
            doctor=self.doctor,
            day=Faker().date_between(start_date='today', end_date='+1y'),
            schedule=['08:00', '08:30', '09:00', '09:30', '14:00']
        )
        self.assertEqual(str(agenda.doctor), self.doctor.name)
        self.assertGreaterEqual(agenda.day, datetime.date.today())
        self.assertEqual(len(agenda.schedule), 5)
        self.assertIn(f'Agenda: {str(agenda.doctor)}', str(agenda))


class MedicalAppointmentModelTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            first_name='bruce',
            last_name='wayne',
            email='normal@user.com',
            password='foo'
        )
        specialty = Specialty.objects.create(name='Cardiologia')
        doctor = Doctor.objects.create(
            name='Jane',
            crm=4567,
            email='jane@joe.com',
            phone='+5516992457046',
            specialty=specialty
        )
        self.agenda = Agenda.objects.create(
            doctor=doctor,
            day=Faker().date_between(start_date='today', end_date='+1y'),
            schedule=['08:00', '08:30', '09:00', '09:30', '14:00']
        )

    def test_create_medical_appointment(self):
        ma = MedicalAppointment.objects.create(
            agenda=self.agenda,
            hourly='09:00',
            patient=self.user,
        )
        self.assertIn(f'Agenda: {str(self.agenda.doctor)}', str(ma.agenda))
        self.assertIn(ma.hourly, ma.agenda.schedule)
        self.assertEqual(ma.patient.first_name, self.user.get_short_name())
        self.assertEqual(ma.patient.email, str(self.user))
