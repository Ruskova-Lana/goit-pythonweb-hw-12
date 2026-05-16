from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for returning user data."""
    id: int
    username: str
    email: EmailStr
    avatar: Optional[str] = None
    confirmed: bool
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Schema for authentication tokens."""
    access_token: str
    refresh_token: str
    token_type: str


class ContactBase(BaseModel):
    """Base schema for contact data."""
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str] = None


class ContactCreate(ContactBase):
    """Schema for creating a new contact."""
    pass


class ContactUpdate(BaseModel):
    """Schema for updating an existing contact."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None


class ContactResponse(ContactBase):
    """Schema for returning contact data."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)