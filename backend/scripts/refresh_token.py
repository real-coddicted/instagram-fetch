import logging
import os

import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def refresh_long_lived_token():
    """
    Utility function to refresh the Meta Graph API long-lived token.
    Can be run manually or set up as a cron job to prevent token expiration.
    """
    load_dotenv()

    app_id = os.getenv("APP_ID")
    app_secret = os.getenv("APP_SECRET")
    long_lived_token = os.getenv("LONG_LIVED_TOKEN")

    if not all([app_id, app_secret, long_lived_token]):
        logger.error(
            "Missing APP_ID, APP_SECRET, or LONG_LIVED_TOKEN in environment variables."
        )
        return

    url = "https://graph.facebook.com/v21.0/oauth/access_token"
    params = {"grant_type": "ig_refresh_access_token", "access_token": long_lived_token}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        new_token = data.get("access_token")
        expires_in = data.get("expires_in")

        logger.info(f"Successfully refreshed token. Expires in {expires_in} seconds.")

        # In a real production system, save this to a Secrets Manager.
        # For local dev, you would typically write this back to the .env file.
        # To avoid logging sensitive tokens, the token is not printed here.

    except requests.RequestException as e:
        logger.error(f"Failed to refresh token: {e}")
        if e.response is not None:
            logger.error(e.response.json())


if __name__ == "__main__":
    refresh_long_lived_token()
