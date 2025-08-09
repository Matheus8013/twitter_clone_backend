import pytest
from rest_framework import status
from django.urls import reverse
from users.factories import UserFactory # Importe seu UserFactory

# Decorador para marcar o teste como de banco de dados
@pytest.mark.django_db
def test_user_registration_success(client):
    """
    Testa se um novo usuário pode ser registrado com sucesso.
    """
    # Dados que serão enviados na requisição POST
    # Certifique-se que 'username', 'email', 'password', 'password2'
    # correspondem aos campos do seu serializer
    registration_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "umaSenhaSegura123!",
        "password2": "umaSenhaSegura123!",
        "first_name": "Test",
        "last_name": "User"
    }

    # A URL para o seu endpoint de registro
    # Use reverse para garantir que a URL está correta.
    # O 'user-register' deve corresponder ao 'name' que você deu ao path em users/urls.py
    url = reverse('user-register')

    # Envia a requisição POST
    response = client.post(url, registration_data, format='json')

    # Verifica o status da resposta
    assert response.status_code == status.HTTP_201_CREATED

    # Verifica se os dados do usuário criado estão na resposta (opcional, mas bom)
    assert 'username' in response.data
    assert response.data['username'] == registration_data['username']
    assert 'email' in response.data
    assert response.data['email'] == registration_data['email']
    # Não devemos ver a senha na resposta, pois definimos como write_only=True

    # Verifica se o usuário foi realmente criado no banco de dados
    from users.models import User
    assert User.objects.filter(username=registration_data['username']).exists()

@pytest.mark.django_db
def test_user_registration_password_mismatch(client):
    """
    Testa se o registro falha quando as senhas não coincidem.
    """
    registration_data = {
        "username": "mismatchuser",
        "email": "mismatch@example.com",
        "password": "SenhaF0rtePraTestes!",
        "password2": "SenhaF0rtePraTestes!123" # Senhas diferentes
    }
    url = reverse('user-register')
    response = client.post(url, registration_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'password' in response.data # Verifica se o erro está relacionado à senha
    assert "As senhas devem ser iguais." in response.data['password']

@pytest.mark.django_db
def test_user_registration_missing_field(client):
    """
    Testa se o registro falha quando um campo obrigatório está faltando.
    """
    registration_data = {
        "email": "missing@example.com",
        "password": "SenhaF0rtePraTestes!",
        "password2": "SenhaF0rtePraTestes!"
        # 'username' está faltando
    }
    url = reverse('user-register')
    response = client.post(url, registration_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data
    assert "This field is required." in response.data['username']

@pytest.mark.django_db
def test_user_registration_duplicate_username(client):
    """
    Testa se o registro falha quando o username já existe.
    """
    # Cria um usuário com o factory ANTES do teste
    UserFactory(username="existinguser")

    registration_data = {
        "username": "existinguser", # Username duplicado
        "email": "duplicate@example.com",
        "password": "SenhaF0rtePraTestes!",
        "password2": "SenhaF0rtePraTestes!"
    }
    url = reverse('user-register')
    response = client.post(url, registration_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data
    assert "A user with that username already exists." in response.data['username'][0] # DRF retorna lista para erros de campo