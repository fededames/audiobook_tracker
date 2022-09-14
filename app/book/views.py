"""
Views for book APIs.
"""
from book import serializers
from core.models import Book
from django.shortcuts import render  # noqa
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class BookViewSet(viewsets.ModelViewSet):
    """View for manage book APIs"""

    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
