from pydantic import BaseModel


class ProfileMetrics(BaseModel):
    username: str
    followers_count: int = 0
    follows_count: int = 0
    media_count: int = 0
    biography: str | None = ""
    profile_picture_url: str | None = None


class PostMetrics(BaseModel):
    caption: str | None = None
    like_count: int | None = 0
    comments_count: int | None = 0
    media_type: str
    media_url: str | None = None
    permalink: str
    timestamp: str
