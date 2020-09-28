import time
import datetime

from rest_framework import viewsets
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
