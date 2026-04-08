import pytest
from unittest.mock import patch, AsyncMock
from app.models.user import User
from app.schemas.user import UserCreate


class TestAuthRoutes:
    @pytest.mark.asyncio
    async def test_google_login(self, client):
        response = await client.get("/auth/google/login")
        assert response.status_code == 200
        data = response.json()
        assert "authorization_url" in data
        assert "state" in data

    @pytest.mark.asyncio
    async def test_google_callback_new_user(self, client, db_session):
        with patch('app.routes.auth.google_oauth.get_access_token', new_callable=AsyncMock) as mock_token, \
             patch('app.routes.auth.google_oauth.get_user_info') as mock_info:

            mock_token.return_value = {"access_token": "token123"}
            mock_info.return_value = {
                "id": "123",
                "email": "newuser@example.com",
                "name": "New User",
                "picture": "https://example.com/photo.jpg"
            }

            response = await client.get("/auth/google/callback?code=code123&state=state123")
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"

            # Check if user was created in database
            user = await db_session.get(User, 1)
            assert user is not None
            assert user.email == "newuser@example.com"
            assert user.google_id == "123"

    @pytest.mark.asyncio
    async def test_google_callback_existing_user(self, client, db_session):
        # Create existing user
        existing_user = User(
            email="existing@example.com",
            name="Existing User",
            google_id="456"
        )
        db_session.add(existing_user)
        await db_session.commit()

        # Mock the OAuth functions
        with patch('app.routes.auth.google_oauth.get_access_token', new_callable=AsyncMock) as mock_token, \
             patch('app.routes.auth.google_oauth.get_user_info') as mock_info:

            mock_token.return_value = {"access_token": "token123"}
            mock_info.return_value = {
                "id": "456",
                "email": "existing@example.com",
                "name": "Existing User",
                "picture": "https://example.com/photo.jpg"
            }

            response = await client.get("/auth/google/callback?code=code123&state=state123")
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data

    @pytest.mark.asyncio
    async def test_get_current_user(self, client, db_session):
        # Create a user
        user = User(
            email="test@example.com",
            name="Test User",
            google_id="789"
        )
        db_session.add(user)
        await db_session.commit()

        # Create access token
        from app.auth.jwt import create_access_token
        token = create_access_token({"sub": user.email})

        # Test the endpoint
        response = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"

    @pytest.mark.asyncio
    async def test_get_current_user_no_token(self, client):
        response = await client.get("/auth/me")
        assert response.status_code == 401