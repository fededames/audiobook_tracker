from core.models import Book
from core.request_registry.bestseller_registry import (BestsellerRegistry,
                                                       QueryNYT)
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to get bestsellers books"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write("Fetching bestsellers")

        post_registry = BestsellerRegistry(QueryNYT.url)
        post_registry.request()
        post_registry.filter_new()
        Book.objects.bulk_create(post_registry.new_books)
        self.stdout.write(f"{len(post_registry.new_books)} new books saved")
