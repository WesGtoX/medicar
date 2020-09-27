from django.contrib import admin
from .models import (
    Specialty, Doctor, Agenda, MedicalAppointment
)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'crm']
    list_filter = ['name', 'email', 'crm', 'phone']
    search_fields = ['name', 'email', 'specialty']


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day']
    list_filter = ['doctor', 'day']
    search_fields = ['doctor', 'day']


@admin.register(MedicalAppointment)
class MedicalAppointmentAdmin(admin.ModelAdmin):
    list_display = ['hourly', 'patient', 'agenda']
    list_filter = ['hourly', 'patient', 'agenda']
    search_fields = ['hourly', 'patient', 'agenda']
