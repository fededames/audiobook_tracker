from core.models import Post
from core.request_registry.post_registry import PostRegistry, QueryReddit
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to get information about books from reddit"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write("Fetching reddit posts")
        post_registry = PostRegistry(QueryReddit.url)
        post_registry.request()
        post_registry.filter_new()
        Post.objects.bulk_create(post_registry.new_posts)
        self.stdout.write(f"{len(post_registry.new_posts)} new posts saved")
