from typing import Any
from pydantic import BaseModel, field_validator


class ProfileStats(BaseModel):
    username: str
    followers_count: int = 0
    follows_count: int = 0
    media_count: int = 0
    biography: str | None = ""
    profile_picture_url: str | None = None


class PostStats(BaseModel):
    caption: str | None = None
    like_count: int | None = 0
    comments_count: int | None = 0
    media_type: str
    media_url: str | None = None
    permalink: str
    timestamp: int

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_timestamp(cls, v: Any) -> int:
        if isinstance(v, int):
            return v
        if isinstance(v, str):
            try:
                from datetime import datetime
                # Meta returns e.g. '2023-10-01T12:00:00+0000'
                dt = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S%z")
                return int(dt.timestamp())
            except Exception:
                pass
        return int(v)
