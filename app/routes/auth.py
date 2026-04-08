from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.jwt import create_access_token
from app.auth.oauth import google_oauth
from db.session import get_db
from app.models.user import User
from app.schemas.user import Token, User as UserSchema
from sqlalchemy import select

router = APIRouter()


@router.get("/google/login")
async def google_login():
    authorization_url, state = google_oauth.get_authorization_url()
    return {"authorization_url": authorization_url, "state": state}


@router.get("/google/callback")
async def google_callback(code: str, state: str, db: AsyncSession = Depends(get_db)):
    try:
        token = await google_oauth.get_access_token(code)
        access_token = token['access_token']
        user_info = google_oauth.get_user_info(access_token)

        # Check if user exists
        result = await db.execute(select(User).where(User.google_id == user_info['id']))
        user = result.scalars().first()

        if not user:
            # Create new user
            user = User(
                email=user_info['email'],
                name=user_info['name'],
                google_id=user_info['id'],
                picture=user_info.get('picture')
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)

        # Create JWT token
        access_token = create_access_token(data={"sub": user.email})
        return Token(access_token=access_token, token_type="bearer")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=UserSchema)
async def get_current_user_endpoint(current_user: User = Depends(get_current_user)):
    return current_user