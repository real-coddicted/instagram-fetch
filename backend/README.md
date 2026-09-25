# Instagram Metrics Fetcher - Tier 1

A FastAPI backend that fetches public Business/Creator Instagram profile metrics and recent post metrics using only Meta's official Graph API `business_discovery` edge.

## Scope & Limitations (Tier 1)

**What this API explicitly does NOT do:**
- Fetch Personal (non-Business) account data (architecturally impossible on this tier).
- Fetch Reels view counts for external accounts.
- Guarantee single-post lookup for old/archived posts outside the recent-media window.
- Provide comment *authors* or comment *text* (only `comments_count` is available).

## Setup & Requirements

### 1. Meta App Setup (Manual)
1. Create a Meta Developer account at developers.facebook.com
2. Create a new App of type "Business"
3. Add the "Instagram Graph API" product to the app
4. Convert your own Instagram account to Business or Creator and link it to a Facebook Page you control
5. Generate a short-lived User Access Token via Graph API Explorer
6. Exchange it for a long-lived token (~60 days)
7. Make note of your `IG_BUSINESS_ID`, `APP_ID`, `APP_SECRET`, and `LONG_LIVED_TOKEN`

### 2. Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```env
IG_BUSINESS_ID=your_ig_business_id
APP_ID=your_app_id
APP_SECRET=your_app_secret
LONG_LIVED_TOKEN=your_long_lived_token
```

### 3. Installation
```bash
pip install -r requirements.txt
```

### 4. Running the Server
```bash
uvicorn app.main:app --reload --port 8001
```

## Example Requests

**Profile Metrics Lookup**
```http
GET /profile/nike
```
```json
{
  "username": "nike",
  "followers_count": 305000000,
  "follows_count": 146,
  "media_count": 1205,
  "biography": "Spotlight on athletes and their stories.",
  "profile_picture_url": "https://scontent..."
}
```

**Single Post Metrics Lookup**
```http
GET /post?username=nike&url=https://www.instagram.com/p/CxyZ1/
```
```json
{
  "caption": "Just do it.",
  "like_count": 500213,
  "comments_count": 1500,
  "media_type": "IMAGE",
  "media_url": "https://scontent...",
  "permalink": "https://www.instagram.com/p/CxyZ1/",
  "timestamp": "2023-10-01T12:00:00+0000"
}
```
