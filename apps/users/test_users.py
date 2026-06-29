# from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.users.models import User

@pytest.mark.django_db
def test_user_registration():
    client = APIClient()

    data = {
        "email": "test@example.com",
        "password": "test1234",
        "password_confirm": "test1234",
        "role": "candidate"
    }

    response = client.post(reverse('signup'), data)
    print(response.data)
    assert response.status_code == 201
    print(response.data)

    assert User.objects.filter(email="test@example.com").exists()

@pytest.mark.django_db
def test_login():
    user = User.objects.create_user(
        email="login@test.com",
        password="pass1234",
        role="candidate"
    )

    client = APIClient()
    response = client.post(reverse('login'), {
        "email": "login@test.com",
        "password": "pass1234"
    })

    assert response.status_code == 200
    assert "access" in response.data