from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import CustomUser

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/register/'
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('access', response.data)

    def test_user_login(self):
        # Register first
        self.client.post(self.register_url, self.user_data, format='json')
        # Login
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)