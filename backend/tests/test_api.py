from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.services.metrics_service.GraphAPIClient.get_profile_metrics")
def test_get_profile_endpoint(mock_get_profile):
    mock_get_profile.return_value = {
        "username": "nike",
        "followers_count": 1000,
        "follows_count": 100,
        "media_count": 50,
        "biography": "Just Do It",
        "profile_picture_url": "http://example.com/pic.jpg",
    }

    response = client.get("/profile/nike")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "nike"
    assert data["followers_count"] == 1000


@patch("app.services.metrics_service.GraphAPIClient.find_post_by_permalink")
def test_get_post_endpoint(mock_find_post):
    mock_find_post.return_value = {
        "caption": "New drop!",
        "like_count": 500,
        "comments_count": 25,
        "media_type": "IMAGE",
        "media_url": "http://example.com/post.jpg",
        "permalink": "https://www.instagram.com/p/123/",
        "timestamp": "2023-10-01T12:00:00+0000",
    }

    response = client.get("/post?username=nike&url=https://www.instagram.com/p/123/")
    assert response.status_code == 200
    data = response.json()
    assert data["like_count"] == 500
    assert data["comments_count"] == 25
