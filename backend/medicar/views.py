import time
import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .filters import SpecialtyFilter, DoctorFilter, AgendaFilter
from .models import Specialty, Doctor, Agenda, MedicalAppointment
from .serializers import (
    SpecialtySerializer, DoctorSerializer,
    AgendaSerializer, MedicalAppointmentSerializer
)


class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SpecialtyFilter


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DoctorFilter


class AgendaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AgendaFilter

    def get_queryset(self):
        """
        Sort items in ascending order of date.
        Filter to not list items with past dates or with all times filled.
        """
        date_now = datetime.date.today()
        queryset = Agenda.objects.filter(day__gte=date_now, schedule__len__gt=0)
        time_now = time.strftime("%H:%M:%S")
        for agenda in queryset:
            for schedule in agenda.schedule:
                if time_now > str(schedule) and date_now >= agenda.day:
                    agenda.schedule.remove(schedule)
                    agenda.save()
        return queryset


class MedicalAppointmentViewSet(viewsets.ModelViewSet):
    queryset = MedicalAppointment.objects.all()
    serializer_class = MedicalAppointmentSerializer

    def get_queryset(self):
        """
        Do not display queries for past day and time.
        Sort items in ascending order of the day and time.
        """
        date_now = datetime.date.today()
        time_now = time.strftime("%H:%M:%S")

        queryset = MedicalAppointment.objects.filter(agenda__day__gte=date_now, patient=self.request.user)
        queryset = queryset.order_by('agenda__day', 'hourly')
        return queryset.exclude(agenda__day__exact=date_now, hourly__lte=time_now)

    def create(self, request, *args, **kwargs):
        medical_appointment = MedicalAppointment()
        medical_appointment.patient = request.user

        try:
            # validate that the agenda exists
            agenda = Agenda.objects.get(pk=request.data.get('agenda_id'))
        except Agenda.DoesNotExist as e:
            error = dict(status=400, error={'message': str(e)})
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        hourly = request.data.get('hourly')

        try:
            # validate that the hour has a valid format
            time.strptime(hourly, "%H:%M")
        except ValueError:
            error = dict(
                status=400,
                error={'message': f'O valor {hourly} tem um formato inválido. Deve estar no formato HH:MM.'}
            )
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        date_now, time_now = datetime.date.today(), time.strftime("%H:%M")
        if agenda.day < date_now or (agenda.day == date_now and str(hourly) < time_now):
            # return an error when the query is on a past date or time
            error = dict(status=400, error={'message': 'Não é possível marcar uma consulta em um tempo passado!'})
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        for schedule in agenda.schedule:
            if str(schedule.strftime("%H:%M")) == hourly:
                if MedicalAppointment.objects.filter(agenda__day=agenda.day, hourly=hourly).exists():
                    # return an error when an appointment already exists at the same time
                    error = dict(status=400, error={'message': 'Já existe uma consulta marcada neste horário!'})
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)

                medical_appointment.agenda = agenda
                medical_appointment.hourly = hourly
                medical_appointment.save()

                agenda_schedule = Agenda.objects.filter(schedule__contains=[hourly], id=agenda.id)
                if agenda_schedule.exists():
                    # remove the scheduled time from the calendar
                    agenda_obj = agenda_schedule.first()
                    agenda_obj.schedule.remove(schedule)
                    agenda_obj.save()

                serializer = MedicalAppointmentSerializer(medical_appointment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        error = dict(status=400, error={'message': 'Ocorreu algum erro na tentativa de marcar uma consulta!'})
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        return Response(dict(status=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(dict(status=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(dict(status=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        medical_appointment = MedicalAppointment.objects.filter(pk=kwargs.get('pk'), patient=request.user)

        if medical_appointment.exists():
            appointment = medical_appointment.first()

            date_now, time_now = datetime.date.today(), time.strftime("%H:%M")
            if appointment.agenda.day < date_now or (appointment.agenda.day == date_now and str(appointment.hourly) < time_now):
                # return error when trying to remove a query that has already happened
                error = dict(
                    status=400, error={'message': 'Não é possível desmarcar uma consulta que já foi realizada!'}
                )
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            return super().destroy(request, *args, **kwargs)

        error = dict(status=400, error={'message': 'Consulta inexistente.'})
        return Response(error, status=status.HTTP_404_NOT_FOUND)
