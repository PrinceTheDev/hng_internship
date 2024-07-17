from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_register_user_successfully(self):
        user_data = {
            "userId": "uniqueUserId",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(self.register_url, user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['firstName'], 'John')

    def test_login_user_successfully(self):
        user_data = {
            "userId": "uniqueUserId",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        self.client.post(self.register_url, user_data, format='json')
        login_data = {
            "email": "john.doe@example.com",
            "password": "password123"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('accessToken', response.data['data'])from django.test import TestCase

# Create your tests here.
