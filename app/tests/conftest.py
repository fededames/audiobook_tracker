import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


@pytest.fixture()
def api_client():
    return APIClient()
