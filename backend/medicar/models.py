import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()


class Specialty(models.Model):
    name = models.CharField('Nome', max_length=55, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Especialidade'
        verbose_name_plural = 'Especialidades'
        ordering = ['id', 'name']


class Doctor(models.Model):
    name = models.CharField('Nome', max_length=55, blank=False, null=False)
    crm = models.IntegerField('CRM', blank=False, null=False)
    email = models.EmailField('E-mail', max_length=100)
    phone = models.CharField(
        'Telefone', max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+9999999999999'. Up to 15 digits allowed."
        )]
    )
    specialty = models.ForeignKey(
        Specialty, verbose_name='Especialidade',
        related_name='doctor',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'
        ordering = ['id', 'name']


class Agenda(models.Model):
    doctor = models.OneToOneField(
        Doctor, verbose_name='Médico',
        related_name='agenda',
        on_delete=models.CASCADE
    )
    day = models.DateField('Dia', blank=False, null=False)
    schedule = ArrayField(
        models.TimeField('Horários', blank=False, null=False)
    )

    def clean(self):
        if self.day < datetime.date.today():
            raise ValidationError('Unable to schedule on a past date.')

    def __str__(self):
        return f'Agenda: {self.doctor.name}, data: {self.day}'


class MedicalAppointment(models.Model):
    agenda = models.ForeignKey(
        Agenda, verbose_name='Paciente',
        related_name='agenda_medical_appointment',
        on_delete=models.CASCADE
    )
    hourly = models.TimeField('Horários', blank=False, null=False)
    patient = models.ForeignKey(
        User, verbose_name='Paciente',
        related_name='user_medical_appointment',
        on_delete=models.CASCADE
    )
    scheduling_date = models.DateTimeField('Data de agendamento', auto_now_add=True)
