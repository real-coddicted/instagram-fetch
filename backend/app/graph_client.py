import logging
from typing import Any

import requests

from app.config import (
    GRAPH_API_BASE_URL,
    GRAPH_API_VERSION,
    IG_BUSINESS_ID,
    LONG_LIVED_TOKEN,
)

logger = logging.getLogger(__name__)


class GraphAPIError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class GraphAPIClient:
    def __init__(self, ig_business_id: str | None = None, access_token: str | None = None):
        self.base_url = f"{GRAPH_API_BASE_URL}/{GRAPH_API_VERSION}"
        self.ig_business_id = ig_business_id or IG_BUSINESS_ID
        self.access_token = access_token or LONG_LIVED_TOKEN
        self.session = requests.Session()
        if self.access_token:
            self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})

    def _raise_for_graph_error(self, response: requests.Response):
        try:
            data = response.json()
        except ValueError:
            raise GraphAPIError(message="Invalid JSON response from Meta", status_code=502)

        if "error" in data:
            error_info = data["error"]
            error_type = error_info.get("type", "")
            error_code = error_info.get("code", 0)
            error_message = error_info.get("message", "Unknown Graph API Error")

            if error_code in (4, 17, 32):
                raise GraphAPIError(
                    message=f"Rate Limit Exceeded: {error_message}", status_code=429
                )

            if (
                error_code == 110
                or "Invalid user id" in error_message
                or error_type == "GraphMethodException"
            ):
                raise GraphAPIError(
                    message="Account not eligible for Business Discovery or doesn't exist",
                    status_code=404,
                )

            if error_type == "OAuthException" or error_code == 190:
                raise GraphAPIError(
                    message=f"OAuth/Auth Error: {error_message}", status_code=400
                )

            raise GraphAPIError(
                message=f"Graph API Error: {error_message}",
                status_code=502,
            )

        if response.status_code != 200:
            raise GraphAPIError(message=f"Unexpected status: {response.status_code}", status_code=502)
        return data

    def _execute_request_with_retry(
        self, url: str, params: dict[str, Any]
    ) -> dict[str, Any]:
        max_retries = 3
        backoff_factor = 2

        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params=params)
            except requests.RequestException:
                raise GraphAPIError(message="Connection to Meta failed", status_code=502)

            try:
                data = self._raise_for_graph_error(response)
                return data
            except GraphAPIError as e:
                if e.status_code == 429 and attempt < max_retries - 1:
                    sleep_time = backoff_factor**attempt
                    logger.warning(f"Rate limited. Retrying in {sleep_time} seconds...")
                    import time

                    time.sleep(sleep_time)
                else:
                    raise
        return {}

    def get_profile_metrics(self, username: str) -> dict[str, Any]:
        url = f"{self.base_url}/{self.ig_business_id}"
        fields = f"business_discovery.username({username}){{username,followers_count,follows_count,media_count,biography,profile_picture_url}}"

        params = {"fields": fields}

        data = self._execute_request_with_retry(url, params)

        if not data or "business_discovery" not in data:
            raise GraphAPIError(
                message="Account not publicly discoverable", status_code=404
            )

        return data["business_discovery"]

    def get_recent_posts(self, username: str, limit: int = 50) -> list[dict[str, Any]]:
        url = f"{self.base_url}/{self.ig_business_id}"
        fields = f"business_discovery.username({username}){{media.limit({limit}){{caption,like_count,comments_count,media_type,media_url,permalink,timestamp}}}}"

        params = {"fields": fields}

        data = self._execute_request_with_retry(url, params)

        if not data or "business_discovery" not in data:
            raise GraphAPIError(
                message="Account not publicly discoverable", status_code=404
            )

        media = data["business_discovery"].get("media", {})
        return media.get("data", [])

    def find_post_by_permalink(
        self, username: str, post_url: str
    ) -> dict[str, Any] | None:
        posts = self.get_recent_posts(username, limit=50)
        target_url = post_url.rstrip("/")

        for post in posts:
            permalink = post.get("permalink", "").rstrip("/")
            if permalink == target_url:
                return post

        return None
