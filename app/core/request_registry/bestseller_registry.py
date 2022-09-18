import os
from dataclasses import dataclass
from typing import Dict

import requests
from book.serializers import BookSerializer
from core import RegistryFromRequest
from core.models import Book

API_KEY = os.getenv("NYT_KEY")


@dataclass
class QueryNYT:
    book_list = "business-books"
    url = (
        f"http://api.nytimes.com/svc/books/v3/lists/current/"
        f"{book_list}.json?api-key={API_KEY}"
    )


class BestsellerRegistry(RegistryFromRequest):
    def __init__(self, url: str):
        self.received_books = []
        self.new_books = []
        self.books_in_db = []
        self.url = url

    def request(self):
        """Request books from url"""
        response = requests.get(self.url)
        return response.json()["results"]["books"]

    def filter_new(self):
        """Get the new posts which are not included"""
        self.books_in_db = BookSerializer(Book.objects.all(), many=True).data
        for book in self.received_books:
            if not self._not_in_db(book):
                self.new_books.append(
                    Book(title=book["title"].lower(), author=book["author"])
                )

    def _not_in_db(self, book: Dict):
        """Return if book is already in DB"""
        for stored_book in BookSerializer(self.posts_in_db, many=True).data:
            if book["title"].lower() in stored_book["title"]:
                return True
        return False
