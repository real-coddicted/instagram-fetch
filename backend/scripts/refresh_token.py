import logging
import os

import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def refresh_long_lived_token():
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
        logger.info(f"New token: {new_token}")

        # In a real production system, save this to a Secrets Manager.
        # For local dev, we just log it or suggest updating .env
        print("\n=== NEW LONG LIVED TOKEN ===")
        print(new_token)
        print("============================\n")

    except requests.RequestException as e:
        logger.error(f"Failed to refresh token: {e}")
        if e.response is not None:
            logger.error(e.response.json())


if __name__ == "__main__":
    refresh_long_lived_token()
