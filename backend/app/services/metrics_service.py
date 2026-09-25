from typing import Any

from app.cache.cache import cache
from app.config import ERROR_TTL, MEDIA_TTL, POST_TTL, PROFILE_TTL
from app.graph_client import GraphAPIClient, GraphAPIError


class MetricsService:
    def __init__(self) -> None:
        self.client = GraphAPIClient()
        self.profile_ttl = PROFILE_TTL
        self.post_ttl = POST_TTL
        self.media_ttl = MEDIA_TTL
        self.error_ttl = ERROR_TTL

    def get_profile(self, username: str) -> dict[str, Any]:
        cache_key = f"profile:{username}"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            if isinstance(cached_data, Exception):
                raise cached_data
            return cached_data

        try:
            data = self.client.get_profile_metrics(username)
            cache.set(cache_key, data, self.profile_ttl)
            return data
        except GraphAPIError as e:
            cache.set(cache_key, e, self.error_ttl)
            raise

    def get_post(self, username: str, post_url: str) -> dict[str, Any]:
        cache_key = f"post:{username}:{post_url}"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            if isinstance(cached_data, Exception):
                raise cached_data
            return cached_data

        try:
            post_data = self.client.find_post_by_permalink(username, post_url)
            if post_data is None:
                error = GraphAPIError(
                    message="Post not found or outside recent-media window",
                    status_code=404,
                )
                cache.set(cache_key, error, self.error_ttl)
                raise error
                
            cache.set(cache_key, post_data, self.post_ttl)
            return post_data
        except GraphAPIError as e:
            cache.set(cache_key, e, self.error_ttl)
            raise

    def get_recent_posts(self, username: str, limit: int = 12) -> list[dict[str, Any]]:
        cache_key = f"recent_posts:{username}:{limit}"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            if isinstance(cached_data, Exception):
                raise cached_data
            return cached_data

        try:
            posts = self.client.get_recent_posts(username, limit=limit)
            cache.set(cache_key, posts, self.media_ttl)
            return posts
        except GraphAPIError as e:
            cache.set(cache_key, e, self.error_ttl)
            raise
