import pytest
import responses

from app.graph_client import GraphAPIClient, GraphAPIError


@pytest.fixture
def client():
    return GraphAPIClient(ig_business_id="12345", access_token="fake_token")


@responses.activate
def test_get_profile_metrics_success(client):
    mock_response = {
        "business_discovery": {
            "username": "nike",
            "followers_count": 1000,
            "follows_count": 100,
            "media_count": 50,
            "biography": "Just Do It",
            "profile_picture_url": "http://example.com/pic.jpg",
        },
        "id": "12345",
    }
    responses.add(
        responses.GET, f"{client.base_url}/12345", json=mock_response, status=200
    )

    data = client.get_profile_metrics("nike")
    assert data["username"] == "nike"
    assert data["followers_count"] == 1000


@responses.activate
def test_get_recent_posts_success(client):
    mock_response = {
        "business_discovery": {
            "media": {
                "data": [
                    {
                        "caption": "New shoes!",
                        "like_count": 10,
                        "comments_count": 2,
                        "media_type": "IMAGE",
                        "media_url": "http://example.com/shoe.jpg",
                        "permalink": "https://www.instagram.com/p/123/",
                        "timestamp": "2023-10-01T12:00:00+0000",
                    }
                ]
            }
        },
        "id": "12345",
    }
    responses.add(
        responses.GET, f"{client.base_url}/12345", json=mock_response, status=200
    )

    posts = client.get_recent_posts("nike")
    assert len(posts) == 1
    assert posts[0]["permalink"] == "https://www.instagram.com/p/123/"


@responses.activate
def test_find_post_by_permalink(client):
    mock_response = {
        "business_discovery": {
            "media": {
                "data": [
                    {"permalink": "https://www.instagram.com/p/123/", "like_count": 10},
                    {"permalink": "https://www.instagram.com/p/456/", "like_count": 20},
                ]
            }
        },
        "id": "12345",
    }
    responses.add(
        responses.GET, f"{client.base_url}/12345", json=mock_response, status=200
    )

    # Test match
    post = client.find_post_by_permalink("nike", "https://www.instagram.com/p/123")
    assert post is not None
    assert post["like_count"] == 10

    # Test no match
    post = client.find_post_by_permalink("nike", "https://www.instagram.com/p/999")
    assert post is None


@responses.activate
def test_oauth_exception(client):
    mock_response = {
        "error": {
            "message": "Error validating access token: Session has expired",
            "type": "OAuthException",
            "code": 190,
        }
    }
    responses.add(
        responses.GET, f"{client.base_url}/12345", json=mock_response, status=401
    )

    with pytest.raises(GraphAPIError) as exc:
        client.get_profile_metrics("nike")
    assert exc.value.status_code == 400
    assert "OAuth/Auth Error" in exc.value.message


@responses.activate
def test_graph_method_exception(client):
    mock_response = {
        "error": {
            "message": "Unsupported get request. Object with ID '123' does not exist",
            "type": "GraphMethodException",
            "code": 100,
        }
    }
    responses.add(
        responses.GET, f"{client.base_url}/12345", json=mock_response, status=400
    )

    with pytest.raises(GraphAPIError) as exc:
        client.get_profile_metrics("personal_account")
    assert exc.value.status_code == 404
    assert "Account not eligible" in exc.value.message


@responses.activate
def test_rate_limit_exception(client):
    mock_response = {
        "error": {
            "message": "Application request limit reached",
            "type": "OAuthException",
            "code": 4,
        }
    }
    responses.add(
        responses.GET, f"{client.base_url}/12345", json=mock_response, status=403
    )

    with pytest.raises(GraphAPIError) as exc:
        client.get_profile_metrics("nike")
    assert exc.value.status_code == 429
    assert "Rate Limit Exceeded" in exc.value.message


@responses.activate
def test_private_account(client):
    mock_response = {
        "id": "12345"
        # business_discovery is missing
    }
    responses.add(
        responses.GET, f"{client.base_url}/12345", json=mock_response, status=200
    )

    with pytest.raises(GraphAPIError) as exc:
        client.get_profile_metrics("private_account")
    assert exc.value.status_code == 404
    assert "Account not publicly discoverable" in exc.value.message
@responses.activate
def test_no_token_leak(client):
    responses.add(
        responses.GET, f"{client.base_url}/12345", body="Not JSON", status=500
    )

    with pytest.raises(GraphAPIError) as exc:
        client.get_profile_metrics("nike")

    assert "fake_token" not in str(exc.value)
    assert exc.value.status_code == 502

