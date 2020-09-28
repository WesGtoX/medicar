from django_filters import rest_framework as filters
from .models import Specialty, Doctor


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
