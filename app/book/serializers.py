from core.models import Book, Note, Post
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    """Serializer for books."""

    class Meta:
        model = Book
        fields = ["id", "title", "author"]
        read_only_fields = ["id"]


class NoteSerializer(serializers.ModelSerializer):
    """Serializer for notes."""

    class Meta:
        model = Note
        fields = ["id", "title", "book_id", "from_minute", "to_minute", "details"]
        read_only_fields = ["id"]


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts."""

    class Meta:
        model = Post
        fields = ["id", "title", "url", "score", "comments"]
        read_only_fields = ["id"]
