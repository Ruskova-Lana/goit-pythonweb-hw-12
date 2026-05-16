from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from goit_hw_12.database import Base


class User(Base):
    """
    Database model for a user.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    role = Column(String(20), default="user")
    refresh_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    contacts = relationship("Contact", back_populates="user")


class Contact(Base):
    """
    Database model for a contact.
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, index=True)
    phone = Column(String(30), nullable=False)
    birthday = Column(Date, nullable=False)
    additional_info = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="contacts")