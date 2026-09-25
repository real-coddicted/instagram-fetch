import os

import pytest

from app.services.metrics_service import MetricsService

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_LIVE_API_TESTS") != "1",
    reason="Live API tests skipped unless RUN_LIVE_API_TESTS=1",
)


def test_live_profile():
    service = MetricsService()
    profile = service.get_profile("nike")
    assert profile["username"] == "nike"
    assert "followers_count" in profile


def test_live_post():
    service = MetricsService()
    recent_posts = service.client.get_recent_posts("nike", limit=1)
    if recent_posts:
        target_url = recent_posts[0]["permalink"]
        post = service.get_post("nike", target_url)
        assert "like_count" in post
        assert "comments_count" in post
