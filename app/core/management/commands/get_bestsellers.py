import json
import os
from typing import Dict, List

import requests
from book.serializers import BookSerializer
from core.models import Book
from django.core.management.base import BaseCommand

API_KEY = os.getenv("NYT_KEY")
REQUESTED_BOOK_LISTS = ("business-books",)


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write("Fetching bestsellers")

        for list in REQUESTED_BOOK_LISTS:
            url = f"http://api.nytimes.com/svc/books/v3/lists/current/{list}.json?api-key={API_KEY}"
            response = requests.get(url)
            books = json.loads(response.text)["results"]["books"]
            new_books = filter_new_bestsellers(books)

            Book.objects.bulk_create(new_books)
            print("done")


def filter_new_bestsellers(books: List[Dict]):
    stored_books = BookSerializer(Book.objects.all(), many=True).data
    new_books = []
    for book in books:
        found = False
        for stored_book in stored_books:
            if book["title"].lower() in stored_book["title"]:
                found = True
                break
        if not found:
            new_books.append(Book(title=book["title"].lower(), author=book["author"]))
    return new_books
