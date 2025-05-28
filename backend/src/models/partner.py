"""
Partner model for spiritual reading providers.
"""

from typing import Optional

from sqlalchemy import String, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Partner(BaseModel):
    """Partner model for reading providers."""
    
    __tablename__ = "partners"
    
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    
    slug: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    website: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    bio: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    photo_url: Mapped[Optional[str]] = mapped_column(
        String(500),
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
    
    # Revenue sharing
    revenue_share_percentage: Mapped[float] = mapped_column(
        default=70.0,  # 70% to partner, 30% to platform
        nullable=False,
    )
    
    # Custom configuration
    custom_rules: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    prompt_stub: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Relationships
    user = relationship("User", back_populates="partner")
    personas = relationship("Persona", back_populates="partner")
    decks = relationship("Deck", back_populates="partner")
    spreads = relationship("Spread", back_populates="partner")
    readings = relationship("Reading", back_populates="partner")
    payments = relationship("Payment", back_populates="partner")
    
    def __repr__(self) -> str:
        return f"<Partner(slug='{self.slug}', name='{self.name}')>"
