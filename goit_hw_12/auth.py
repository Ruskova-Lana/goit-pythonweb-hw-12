from datetime import datetime, timedelta, timezone
from typing import Optional
import json

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from goit_hw_12.database import get_db
from goit_hw_12.email_service import (
    send_password_reset_email,
    send_verification_email,
)
from goit_hw_12.models import User
from goit_hw_12.redis_client import redis_client
from goit_hw_12.schemas import UserCreate, UserResponse
from goit_hw_12.config import settings


router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password, hashed_password):
    """
    Verify password against hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hash user password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[int] = None):
    """
    Create JWT access token.

    :param data: Data to encode in the token.
    :param expires_delta: Optional expiration time in minutes.
    :return: Encoded JWT access token.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[int] = None):
    """
    Create JWT refresh token.

    :param data: Data to encode in the token.
    :param expires_delta: Optional expiration time in days.
    :return: Encoded JWT refresh token.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        days=expires_delta or 7
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def create_email_token(email: str):
    """
    Create email verification token.
    """
    expire = datetime.now(timezone.utc) + timedelta(days=1)

    to_encode = {
        "sub": email,
        "exp": expire,
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_password_reset_token(email: str):
    """
    Create password reset token.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode = {
        "sub": email,
        "type": "password_reset",
        "exp": expire,
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Retrieve the currently authenticated user from Redis cache or database.

    If the user is present in Redis cache, the function returns a User-like
    object without querying the database. If the user is not cached, the
    function retrieves the user from PostgreSQL and stores minimal safe user
    data in Redis.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    cached_user = redis_client.get(f"user:{email}")

    if cached_user:
        user_data = json.loads(cached_user)

        return User(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data["email"],
            avatar=user_data.get("avatar"),
            confirmed=user_data["confirmed"],
            role=user_data["role"],
        )

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    redis_client.setex(
        f"user:{email}",
        900,
        json.dumps(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "avatar": user.avatar,
                "confirmed": user.confirmed,
                "role": user.role,
            }
        ),
    )

    return user


def admin_required(
    current_user: User = Depends(get_current_user),
):
    """
    Check admin role.
    """

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    body: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Register new user.
    """

    existing_user = (
        db.query(User)
        .filter(User.email == body.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
        )

    hashed_password = get_password_hash(body.password)

    new_user = User(
        username=body.username,
        email=body.email,
        password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_email_token(new_user.email)

    background_tasks.add_task(
        send_verification_email,
        new_user.email,
        token,
    )

    return new_user


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return JWT access and refresh tokens.

    :param form_data: OAuth2 password request form data.
    :param db: Database session.
    :return: Dictionary containing access token, refresh token, and token type.
    """

    user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(
        form_data.password,
        user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email is not confirmed",
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email}
    )
    user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/refresh_token")
async def refresh_token(
    refresh_token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Refresh access token using refresh token.

    :param refresh_token: The refresh token to use (passed as Bearer token).
    :param db: Database session.
    :return: Dictionary containing new access token, refresh token, and token type.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None or user.refresh_token != refresh_token:
        raise credentials_exception

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/confirmed_email/{token}")
async def confirmed_email(
    token: str,
    db: Session = Depends(get_db),
):
    """
    Confirm user email.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        email = payload.get("sub")

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.confirmed = True

    db.commit()

    redis_client.delete(f"user:{user.email}")

    return {"message": "Email confirmed"}


@router.post("/request-password-reset")
async def request_password_reset(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Request password reset email.
    """

    user = db.query(User).filter(User.email == email).first()

    if user:
        token = create_password_reset_token(user.email)

        background_tasks.add_task(
            send_password_reset_email,
            user.email,
            token,
        )

    return {
        "message": (
            "If this email exists, "
            "password reset instructions were sent"
        )
    }


@router.post("/reset-password/{token}")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db),
):
    """
    Reset user password.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        email = payload.get("sub")

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.password = get_password_hash(new_password)

    db.commit()

    redis_client.delete(f"user:{user.email}")

    return {"message": "Password updated successfully"}