import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from app.models import UserRole

# Base User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = Field(default=None, max_length=255)
    role: UserRole = Field(default=UserRole.USER)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    role: UserRole | None = None

class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Authentication Token Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    user_id: uuid.UUID | None = None

# Custom JSON Login (Optional fallback to OAuth2 standard form)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

