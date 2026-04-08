import pytest
from unittest.mock import AsyncMock, patch
from app.auth.jwt import create_access_token, verify_token
from app.auth.oauth import google_oauth
from app.models.user import User
from app.schemas.user import UserCreate


class TestJWT:
    def test_create_access_token(self):
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_token_valid(self):
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        email = verify_token(token, Exception("Invalid token"))
        assert email == "test@example.com"

    def test_verify_token_invalid(self):
        with pytest.raises(Exception):
            verify_token("invalid_token", Exception("Invalid token"))


class TestGoogleOAuth:
    def test_get_authorization_url(self):
        with patch('app.auth.oauth.OAuth2Session') as mock_client:
            from unittest.mock import Mock
            mock_instance = Mock()
            mock_instance.create_authorization_url.return_value = ("https://example.com/auth", "state123")
            mock_client.return_value = mock_instance

            url, state = google_oauth.get_authorization_url()
            assert url == "https://example.com/auth"
            assert state == "state123"

    @pytest.mark.asyncio
    async def test_get_access_token(self):
        with patch('app.auth.oauth.AsyncOAuth2Client') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.fetch_token.return_value = {"access_token": "token123"}
            mock_client.return_value = mock_instance

            token = await google_oauth.get_access_token("code123")
            assert token["access_token"] == "token123"

    def test_get_user_info(self):
        with patch('app.auth.oauth.requests.get') as mock_get:
            from unittest.mock import Mock
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "id": "123",
                "email": "test@example.com",
                "name": "Test User",
                "picture": "https://example.com/photo.jpg"
            }
            mock_get.return_value = mock_response

            user_info = google_oauth.get_user_info("token123")
            assert user_info["email"] == "test@example.com"
            assert user_info["name"] == "Test User"