import pytest
from django.contrib.auth import get_user_model
from tests.conftest import create_user


@pytest.mark.django_db
def test_create_user_with_email_successful():
    """Test creating a user with an email is successful."""
    email = "test@example.com"
    password = "testpass123"
    user = create_user(
        email=email,
        password=password,
    )

    assert user.email == email
    assert user.check_password(password) is True


@pytest.mark.django_db
def test_new_user_email_normalized():
    """Test email is normalized for new users."""
    sample_emails = [
        ["test1@EXAMPLE.com", "test1@example.com"],
        ["Test2@Example.com", "Test2@example.com"],
        ["TEST3@EXAMPLE.com", "TEST3@example.com"],
        ["test4@example.COM", "test4@example.com"],
    ]
    for email, expected in sample_emails:
        user = create_user(email=email, password="sample123")
        assert user.email == expected


@pytest.mark.django_db
def test_new_user_without_email_raises_error():
    """Test that creating a user without an email raises a ValueError."""
    with pytest.raises(ValueError):
        create_user(email="", password="test123")


@pytest.mark.django_db
def test_create_superuser():
    """Test creating a superuser."""
    user = get_user_model().objects.create_superuser(
        "test@example.com",
        "test123",
    )

    assert user.is_superuser is True
    assert user.is_staff is True
