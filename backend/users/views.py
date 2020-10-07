from django.contrib.auth import get_user_model

from rest_framework import status, viewsets
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        super(UserViewSet, self).create(request, *args, **kwargs)
        return Response({}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        return Response(dict(status=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(dict(status=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(dict(status=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(dict(status=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(dict(status=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CustomObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'name': token.user.get_full_name()})
