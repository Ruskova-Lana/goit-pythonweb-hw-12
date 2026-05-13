from fastapi import APIRouter, Depends, File, Request, UploadFile
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from goit_hw_12.auth import get_current_user, admin_required
from goit_hw_12.cloudinary_service import upload_avatar
from goit_hw_12.database import get_db
from goit_hw_12.models import User
from goit_hw_12.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])

limiter = Limiter(key_func=get_remote_address)


@router.get("/me", response_model=UserResponse)
@limiter.limit("5/minute")
async def get_me(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.patch("/avatar", response_model=UserResponse)
async def update_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(admin_required),
    db: Session = Depends(get_db),
):
    """
    Update user avatar.

    Only users with admin role are allowed to update avatar.
    """
    avatar_url = upload_avatar(file, current_user.id)

    current_user.avatar = avatar_url
    db.commit()
    db.refresh(current_user)

    return current_user