import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


def create_user(email="user@example.com", password="testpass123"):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


@pytest.fixture()
def api_client():
    return APIClient()
