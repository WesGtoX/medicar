from django_filters import rest_framework as filters
from .models import Specialty, Doctor, Agenda


class SpecialtyFilter(filters.FilterSet):
    search = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Specialty
        fields = ['search']


class DoctorFilter(filters.FilterSet):
    search = filters.CharFilter(field_name="name", lookup_expr='icontains')
    specialty = filters.ModelMultipleChoiceFilter(
        queryset=Specialty.objects.all()
    )

    class Meta:
        model = Doctor
        fields = ['search', 'specialty']


class AgendaFilter(filters.FilterSet):
    doctor = filters.ModelMultipleChoiceFilter(
        queryset=Doctor.objects.all()
    )
    specialty = filters.ModelMultipleChoiceFilter(
        field_name='doctor__specialty',
        lookup_expr='exact',
        queryset=Specialty.objects.all()
    )
    start_date = filters.CharFilter(field_name="day", lookup_expr='gte')
    end_date = filters.CharFilter(field_name="day", lookup_expr='lte')

    class Meta:
        model = Agenda
        fields = ['doctor', 'specialty', 'start_date', 'end_date']
