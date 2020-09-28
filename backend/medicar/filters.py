from django_filters import rest_framework as filters
from .models import Specialty


class SpecialtyFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Specialty
        fields = ['name']
