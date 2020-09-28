import factory
from faker import Faker
from medicar.models import (
    Specialty, Doctor, Agenda, MedicalAppointment
)

fake = Faker(['pt_BR'])


class SpecialtyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Specialty

    name = factory.Faker('word', ext_word_list=['Cardiologia', 'Pediatria'])


class DoctorFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Doctor

    name = factory.Faker('first_name')
    crm = factory.Faker('pyint', min_value=1000, max_value=9999, step=1)
    email = factory.Faker('ascii_email')
    phone = f'+{fake.msisdn()}'


class AgendaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Agenda

    day = factory.Faker('date_between', start_date='today', end_date='+1y')
    schedule = ['08:00', '08:30', '09:00', '09:30', '14:00']


class MedicalAppointmentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = MedicalAppointment

    hourly = factory.Faker('word', ext_word_list=['08:00', '08:30', '09:00', '09:30', '14:00'])
