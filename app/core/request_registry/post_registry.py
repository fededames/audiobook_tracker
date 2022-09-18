from dataclasses import dataclass
from typing import Dict, Optional

import requests
from book.serializers import PostSerializer
from core import RegistryFromRequest
from core.models import Post


class TooManyRequestsException(Exception):
    def __init__(self, message="Too many requests sent. Please, wait some minutes"):
        self.message = message
        super().__init__(self.message)


class PostRegistry(RegistryFromRequest):
    """Registry of book posts from Reddit"""

    def __init__(self, url: str):
        self.received_posts = []
        self.new_posts = []
        self.posts_in_db = []
        self.url = url

    def request(self):
        """Request reddit posts"""
        print(self.url)
        response = requests.get(self.url)
        if response.status_code == 429:
            raise TooManyRequestsException
        self.received_posts = response.json()["data"]["children"]

    def filter_new(self):
        """Get the new posts which are not included"""
        self.posts_in_db = PostSerializer(Post.objects.all(), many=True).data
        for post in self.received_posts:
            if not self._not_in_db(post):
                self.new_posts.append(
                    Post(
                        title=post["data"]["title"].lower(),
                        url=post["data"]["url"],
                        score=post["data"]["score"],
                        comments=post["data"]["num_comments"],
                    )
                )

    def _not_in_db(self, post: Dict):
        """Return if post is already in DB"""
        for stored_post in PostSerializer(self.posts_in_db, many=True).data:
            if post["title"].lower() in stored_post["title"]:
                return True
        return False


@dataclass
class QueryReddit:
    """Query Reddit Information"""

    subreddit: Optional[str] = "BettermentBookClub"
    listing_type: Optional[
        str
    ] = "top"  # controversial, best, hot, new, random, rising, top
    limit: Optional[int] = 10
    timeframe: Optional[str] = "year"
    url = f"https://www.reddit.com/r/{subreddit}/{listing_type}.json?limit={limit}&t={timeframe}"  # hour, day, week, month, year, all
