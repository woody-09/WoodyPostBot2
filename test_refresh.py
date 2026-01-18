import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Load environment variables
load_dotenv()

def test_refresh():
    client_id = os.getenv("CLIENT_ID") or os.getenv("BLOGGER_CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET") or os.getenv("BLOGGER_CLIENT_SECRET")
    refresh_token = os.getenv("REFRESH_TOKEN") or os.getenv("BLOGGER_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("Missing credentials in .env")
        return

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )

    try:
        print("Attempting to refresh access token...")
        creds.refresh(Request())
        print("SUCCESS: Token refreshed successfully!")
        print(f"New Access Token: {creds.token[:10]}...")
    except Exception as e:
        print(f"FAILED: Token refresh failed: {e}")
        if 'invalid_grant' in str(e):
            print("\nDiagnosis: The refresh token is invalid or has been revoked.")
            print("Possible reasons:")
            print("1. The Google Cloud project is in 'Testing' mode (tokens expire in 7 days).")
            print("2. The user has revoked access in their Google Account settings.")
            print("3. The client ID or secret has changed.")
            print("\nAction: Run 'python get_token.py' to get a new refresh token.")

if __name__ == "__main__":
    test_refresh()
