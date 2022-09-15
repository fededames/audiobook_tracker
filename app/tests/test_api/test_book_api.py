import pytest
from book.serializers import BookSerializer
from core.models import Book
from django.urls import reverse
from rest_framework import status
from tests.conftest import create_user

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
BOOKS_URL = reverse("book:book-list")


def create_book(**params):
    """Create and return a sample book."""
    defaults = {
        "title": "Sample title",
        "author": "Sample author",
    }
    defaults.update(params)

    book = Book.objects.create(**defaults)
    return book


@pytest.mark.django_db
def test_auth_required(api_client):
    """Test auth is required to call API"""
    res = api_client.get(BOOKS_URL)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_retrieve_books(api_client):
    """Test retrieving list of books"""
    user = create_user(email="user@example.com", password="testpass123")
    api_client.force_authenticate(user)
    create_book()
    res = api_client.get(BOOKS_URL)
    books = Book.objects.all().order_by("-id")
    serializer = BookSerializer(books, many=True)
    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
