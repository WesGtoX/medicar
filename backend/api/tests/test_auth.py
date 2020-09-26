from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthTokenTests(APITestCase):

    def setUp(self):
        """create a valid user"""
        self.data = {'email': 'bruce@wayne.com', 'password': 'imbatman'}
        self.user = User.objects.create_user(
            email=self.data['email'],
            password=self.data['password']
        )

    def test_token_login(self):
        """post to get token"""
        response = self.client.post(
            reverse('api_token_auth'),
            data={
                'username': self.data['email'],
                'password': self.data['password']
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token', response.data)
