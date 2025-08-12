import pytest
from rest_framework import status
from django.urls import reverse
from users.factories import UserFactory

@pytest.mark.django_db
def test_user_registration_success(client):
    registration_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "umaSenhaSegura123!",
        "password2": "umaSenhaSegura123!",
        "first_name": "Test",
        "last_name": "User"
    }

    url = reverse('users:user-register')

    response = client.post(url, registration_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED

    assert 'username' in response.data
    assert response.data['username'] == registration_data['username']
    assert 'email' in response.data
    assert response.data['email'] == registration_data['email']

    from users.models import User
    assert User.objects.filter(username=registration_data['username']).exists()

@pytest.mark.django_db
def test_user_registration_password_mismatch(client):

    registration_data = {
        "username": "mismatchuser",
        "email": "mismatch@example.com",
        "password": "SenhaF0rtePraTestes!",
        "password2": "SenhaF0rtePraTestes!123"
    }
    url = reverse('users:user-register')
    response = client.post(url, registration_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'password' in response.data
    assert "As senhas devem ser iguais." in response.data['password']

@pytest.mark.django_db
def test_user_registration_missing_field(client):

    registration_data = {
        "email": "missing@example.com",
        "password": "SenhaF0rtePraTestes!",
        "password2": "SenhaF0rtePraTestes!"
    }
    url = reverse('users:user-register')
    response = client.post(url, registration_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data
    assert "This field is required." in response.data['username']

@pytest.mark.django_db
def test_user_registration_duplicate_username(client):

    UserFactory(username="existinguser")

    registration_data = {
        "username": "existinguser", # Username duplicado
        "email": "duplicate@example.com",
        "password": "SenhaF0rtePraTestes!",
        "password2": "SenhaF0rtePraTestes!"
    }
    url = reverse('users:user-register')
    response = client.post(url, registration_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data
    assert "A user with that username already exists." in response.data['username'][0]