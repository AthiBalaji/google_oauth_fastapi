import requests
from authlib.integrations.base_client import OAuthError
from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.integrations.requests_client import OAuth2Session

from core.config import settings


class GoogleOAuth:
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI

    def get_authorization_url(self):
        client = OAuth2Session(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
        )
        authorization_url, state = client.create_authorization_url(
            'https://accounts.google.com/o/oauth2/auth',
            scope=['openid', 'email', 'profile'],
        )
        return authorization_url, state

    async def get_access_token(self, code: str):
        client = AsyncOAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
        )
        try:
            token = await client.fetch_token(
                'https://oauth2.googleapis.com/token',
                code=code,
            )
            return token
        except OAuthError as e:
            raise Exception(f"OAuth error: {e}")

    def get_user_info(self, access_token: str):
        url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch user info")


google_oauth = GoogleOAuth()