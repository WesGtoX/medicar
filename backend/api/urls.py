from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from users.views import UserViewSet
from medicar.views import (
    SpecialtyViewSet, DoctorViewSet,
    AgendaViewSet, MedicalAppointmentViewSet
)

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('especialidades', SpecialtyViewSet)
router.register('medicos', DoctorViewSet)
router.register('agendas', AgendaViewSet)
router.register('consultas', MedicalAppointmentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls')),
]
