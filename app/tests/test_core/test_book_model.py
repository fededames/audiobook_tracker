import pytest
from core import models


@pytest.mark.django_db
def test_create_book():
    """Test creating a book is successful."""
    book = models.Book.objects.create(
        title="Book name",
        author="Author name",
    )

    assert str(book) == book.title
