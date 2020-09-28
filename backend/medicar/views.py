from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .filters import SpecialtyFilter, DoctorFilter
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


class MedicalAppointmentViewSet(viewsets.ModelViewSet):
    queryset = MedicalAppointment.objects.all()
    serializer_class = MedicalAppointmentSerializer
