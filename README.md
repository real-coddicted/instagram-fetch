# Instagram Metrics Fetcher

A full-stack application that fetches and displays public Business/Creator Instagram profile metrics and recent post metrics using Meta's official Graph API (`business_discovery` edge).

## 🚀 Features
- **Profile Metrics**: Fetch follower count, follows count, media count, biography, and profile picture.
- **Post Metrics**: Fetch like count, comment count, and timestamp for a specific post URL.
- **Backend**: Built with Python & FastAPI.
- **Frontend**: Built with React & Vite.

---

## 🔑 How to Get Your Meta API Tokens
This project relies on the **Instagram Graph API**. You must provide your own credentials to run this code, as tokens are secret and not checked into version control.

Follow these steps exactly to generate the required environment variables:

### Step 1: Create a Meta Developer App
1. Go to [Meta for Developers](https://developers.facebook.com/) and log in.
2. Click **My Apps** -> **Create App**.
3. Select **Other** -> **Next**.
4. Select **Business** as the app type -> **Next**.
5. Give your app a name and click **Create App**.

### Step 2: Set up the Instagram Graph API
1. In your App Dashboard, scroll down to the **Add products to your app** section.
2. Find **Instagram Graph API** and click **Set Up**.
3. Your app now has access to the Graph API. 

### Step 3: Link Your Accounts
*The API requires an Instagram Business or Creator account connected to a Facebook Page you manage.*
1. Make sure your Instagram account is set to **Professional (Business or Creator)** in the app settings.
2. Connect your Instagram account to a Facebook Page that you are an admin of.

### Step 4: Generate a User Access Token
1. Go to the [Graph API Explorer](https://developers.facebook.com/tools/explorer/).
2. In the right panel, select your App from the **Meta App** dropdown.
3. Under **User or Page**, select **Get User Access Token**.
4. A popup will ask you to grant permissions. You MUST grant the following permissions:
   - `instagram_basic`
   - `instagram_manage_insights`
   - `pages_show_list`
   - `pages_read_engagement`
5. Click **Generate Access Token**. This gives you a **Short-Lived Token** (valid for ~1 hour).

### Step 5: Get a Long-Lived Access Token (Recommended)
Since the short-lived token expires quickly, exchange it for a 60-day token:
1. In the Graph API Explorer, click the **info icon (i)** next to the Access Token you just generated.
2. Click **Open in Access Token Tool**.
3. Scroll down and click **Extend Access Token**.
4. Copy this new token. This is your `LONG_LIVED_TOKEN`.

### Step 6: Find Your IG Business ID
1. Go back to the Graph API Explorer.
2. Enter `me/accounts?fields=instagram_business_account` in the request URL bar and hit Submit.
3. The JSON response will contain an `instagram_business_account` object with an `id`.
4. Copy this `id`. This is your `IG_BUSINESS_ID`.

### Step 7: Get App ID and Secret
1. Go back to your App Dashboard on Meta for Developers.
2. In the left sidebar, go to **App Settings** -> **Basic**.
3. Here you will find your **App ID** (`APP_ID`) and **App Secret** (`APP_SECRET`). (Click "Show" to reveal the secret).

---

## 💻 Setup & Installation

### 1. Backend Setup
1. Open a terminal and navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create your environment variables file:
   ```bash
   cp .env.example .env
   ```
3. Open the `.env` file and fill in the credentials you gathered above:
   ```env
   IG_BUSINESS_ID=your_ig_business_id
   APP_ID=your_app_id
   APP_SECRET=your_app_secret
   LONG_LIVED_TOKEN=your_long_lived_token
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the server:
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

### 2. Frontend Setup
1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the frontend development server:
   ```bash
   npm run dev
   ```

Your browser will now open the application, and you can start fetching metrics!
