from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dependencies import get_db, get_current_user
from app.models import User
from app.schemas import UserResponse, UserUpdate
from app.security import get_password_hash

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Retrieve details of the currently logged-in user."""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update profile details of the currently logged-in user."""
    # If updating email, verify it's not already in use by another user
    if user_update.email is not None and user_update.email != current_user.email:
        result = await db.execute(select(User).filter(User.email == user_update.email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )
        current_user.email = user_update.email

    # Update full name if supplied
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name

    # Update password if supplied (hash it first)
    if user_update.password is not None:
        current_user.password_hash = get_password_hash(user_update.password)

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user
