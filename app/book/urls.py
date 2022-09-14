"""
URL mappings for the book app.
"""


from book import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("books", views.BookViewSet)

app_name = "book"

urlpatterns = [
    path("", include(router.urls)),
]
