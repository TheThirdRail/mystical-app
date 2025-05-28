"""
Persona model for partner spiritual guides.
"""

from typing import Optional

from sqlalchemy import String, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Persona(BaseModel):
    """Persona model for spiritual guides."""
    
    __tablename__ = "personas"
    
    partner_id: Mapped[str] = mapped_column(
        ForeignKey("partners.id"),
        nullable=False,
        index=True,
    )
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    title: Mapped[Optional[str]] = mapped_column(
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
    
    specialties: Mapped[Optional[list]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    # AI voice customization
    voice_style: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    
    tone: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    
    prompt_prefix: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    prompt_suffix: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Configuration
    custom_rules: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    # Relationships
    partner = relationship("Partner", back_populates="personas")
    readings = relationship("Reading", back_populates="persona")
    
    def __repr__(self) -> str:
        return f"<Persona(name='{self.name}', partner='{self.partner.slug if self.partner else None}')>"
