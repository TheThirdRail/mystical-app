"""
User model for authentication and authorization.
"""

from enum import Enum
from typing import Optional

from sqlalchemy import String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class UserRole(str, Enum):
    """User roles."""
    ADMIN = "admin"
    PARTNER = "partner"
    USER = "user"


class User(BaseModel):
    """User model."""
    
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    
    username: Mapped[Optional[str]] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=True,
    )
    
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    full_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        default=UserRole.USER,
        nullable=False,
    )
    
    # Relationships
    partner = relationship("Partner", back_populates="user", uselist=False)
    readings = relationship("Reading", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(email='{self.email}', role='{self.role}')>"
