from fastapi import APIRouter, Depends, File, Request, UploadFile
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from goit_hw_10.auth import get_current_user
from goit_hw_10.cloudinary_service import upload_avatar
from goit_hw_10.database import get_db
from goit_hw_10.models import User
from goit_hw_10.schemas import UserResponse

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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    avatar_url = upload_avatar(file, current_user.id)

    current_user.avatar = avatar_url
    db.commit()
    db.refresh(current_user)

    return current_user