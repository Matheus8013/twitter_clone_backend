from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.factories import UserFactory

class LoginTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(username='testuser')
        self.login_url = reverse('users:user-login')

    def test_successful_login(self):
        data = {
            'username': 'testuser',
            'password': 'SenhaF0rtePraTestes!'
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertIsInstance(response.data['token'], str)

    def test_login_with_invalid_password(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_missing_password(self):
        data = {
            'username': 'testuser',
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
