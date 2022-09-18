from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Book(models.Model):
    """Book object"""

    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Note(models.Model):
    """Book note"""

    from_minute = models.IntegerField()
    to_minute = models.IntegerField()
    title = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    """Reddit post"""

    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    score = models.IntegerField()
    comments = models.IntegerField()

    def __str__(self):
        return self.title
