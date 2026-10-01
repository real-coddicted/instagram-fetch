from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    IG_BUSINESS_ID: str
    LONG_LIVED_TOKEN: str
    GRAPH_API_BASE_URL: str = "https://graph.facebook.com"
    GRAPH_API_VERSION: str = "v26.0"
    
    PROFILE_TTL: int = 15 * 60
    POST_TTL: int = 15 * 60
    MEDIA_TTL: int = 15 * 60
    ERROR_TTL: int = 5 * 60
    
    ALLOWED_ORIGIN: str = "http://localhost:5173"
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

IG_BUSINESS_ID = settings.IG_BUSINESS_ID
LONG_LIVED_TOKEN = settings.LONG_LIVED_TOKEN
GRAPH_API_BASE_URL = settings.GRAPH_API_BASE_URL
GRAPH_API_VERSION = settings.GRAPH_API_VERSION
PROFILE_TTL = settings.PROFILE_TTL
POST_TTL = settings.POST_TTL
MEDIA_TTL = settings.MEDIA_TTL
ERROR_TTL = settings.ERROR_TTL
ALLOWED_ORIGIN = settings.ALLOWED_ORIGIN
