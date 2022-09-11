import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


@pytest.fixture()
def client():
    return APIClient()


@pytest.mark.django_db
def test_create_user_success(client):
    """Test creating a user is successful."""
    payload = {
        "email": "test@example.com",
        "password": "testpass123",
        "name": "Test Name",
    }
    res = client.post(CREATE_USER_URL, payload)

    assert res.status_code == status.HTTP_201_CREATED
    user = get_user_model().objects.get(email=payload["email"])
    assert user.check_password(payload["password"]) is True
    assert "password" not in res.data


@pytest.mark.django_db
def test_user_with_email_exists_error(client):
    """Test error returned if user with email exists."""
    payload = {
        "email": "test@example.com",
        "password": "testpass123",
        "name": "Test Name",
    }
    create_user(**payload)
    res = client.post(CREATE_USER_URL, payload)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_password_too_short_error(client):
    """Test an error is returned if password less than 5 chars."""
    payload = {
        "email": "test@example.com",
        "password": "pw",
        "name": "Test name",
    }
    res = client.post(CREATE_USER_URL, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
    assert user_exists is False


@pytest.mark.django_db
def test_create_token_for_user(client):
    """Test generates token for valid credentials"""
    user_details = {
        "name": "Test Name",
        "email": "test@example.com",
        "password": "test-user-password123",
    }
    create_user(**user_details)
    payload = {"email": user_details["email"], "password": user_details["password"]}
    res = client.post(TOKEN_URL, payload)
    assert "token" in res.data
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_token_bad_credentials(client):
    """Return error if credentials are invalid"""
    create_user(email="test@example.com", password="goodpass")
    payload = {"email": "test@example.com", "password": "badpass"}
    res = client.post(TOKEN_URL, payload)

    assert "token" not in res.data
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_token_blank_password(client):
    """Return error if password is blank"""
    payload = {"email": "test@example.com", "password": ""}
    res = client.post(TOKEN_URL, payload)

    assert "token" not in res.data
    assert res.status_code == status.HTTP_400_BAD_REQUEST
