"""
Views for book APIs.
"""
from book import serializers
from core.models import Book, Note, Post
from django.shortcuts import render  # noqa
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """View for manage books APIs"""

    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class NoteViewSet(viewsets.ModelViewSet):
    """View for manage notes APIs"""

    serializer_class = serializers.NoteSerializer
    queryset = Note.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create a new note."""
        serializer.save(reader=self.request.user)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """View for manage posts APIs"""

    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
