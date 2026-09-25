import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
LONG_LIVED_TOKEN = os.getenv("LONG_LIVED_TOKEN")
GRAPH_API_BASE_URL = os.getenv("GRAPH_API_BASE_URL", "https://graph.facebook.com")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v26.0")

# Cache TTLs
PROFILE_TTL = int(os.getenv("PROFILE_TTL", str(15 * 60)))
POST_TTL = int(os.getenv("POST_TTL", str(15 * 60)))
MEDIA_TTL = int(os.getenv("MEDIA_TTL", str(15 * 60)))
ERROR_TTL = int(os.getenv("ERROR_TTL", str(5 * 60)))

ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "http://localhost:5173")

if not IG_BUSINESS_ID or not LONG_LIVED_TOKEN:
    logging.getLogger(__name__).critical("FATAL ERROR: IG_BUSINESS_ID and LONG_LIVED_TOKEN must be set in the environment.")
    sys.exit(1)
