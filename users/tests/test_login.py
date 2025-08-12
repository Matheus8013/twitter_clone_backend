from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.factories import UserFactory

class LoginTests(APITestCase):
    def setUp(self):
        # Cria um usuário de teste que será usado em todos os testes
        self.user = UserFactory(username='testuser')
        self.login_url = reverse('users:user-login')  # Use o nome da URL que você definiu

    def test_successful_login(self):
        """Verifica se um usuário pode fazer login com sucesso."""
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
        """Verifica se o login falha com uma senha incorreta."""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_missing_password(self):
        """Verifica se o login falha se a senha for omitida."""
        data = {
            'username': 'testuser',
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
