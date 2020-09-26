from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserViewSetTests(APITestCase):

    def setUp(self):
        """users data do create"""
        self.data = {
            'first_name': 'Bruce',
            'last_name': 'Wayne',
            'email': 'bruce@wayne.com',
            'password': 'imbatman'
        }

    def test_perform_create(self):
        """create a user"""
        response = self.client.post(reverse('user-list'), data=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)

    def test_list(self):
        """get list not allowed"""
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve(self):
        """get detail not allowed"""
        response = self.client.get(reverse('user-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update(self):
        """put update not allowed"""
        response = self.client.put(reverse('user-detail', args=[1], kwargs={}))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update(self):
        """put partial update not allowed"""
        response = self.client.patch(reverse('user-detail', args=[1], kwargs={}))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_destroy(self):
        """destroy not allowed"""
        response = self.client.delete(reverse('user-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
