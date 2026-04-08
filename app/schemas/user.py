from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: str
    picture: str | None = None


class UserCreate(UserBase):
    google_id: str | None = None


class User(UserBase):
    id: int
    google_id: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None