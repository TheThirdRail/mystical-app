"""
Spread model for tarot card layouts.
"""

from typing import Optional

from sqlalchemy import String, Text, Boolean, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Spread(BaseModel):
    """Tarot spread model."""
    
    __tablename__ = "spreads"
    
    partner_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("partners.id"),
        nullable=True,
        index=True,
    )
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Spread configuration
    card_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    
    positions: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
    )
    
    # Position format:
    # [
    #   {
    #     "name": "Past",
    #     "description": "What influences from the past affect this situation",
    #     "x": 0,
    #     "y": 0,
    #     "rotation": 0
    #   },
    #   ...
    # ]
    
    # Usage instructions
    instructions: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Difficulty level
    difficulty: Mapped[str] = mapped_column(
        String(20),
        default="beginner",
        nullable=False,  # beginner, intermediate, advanced
    )
    
    # Categories/tags
    categories: Mapped[Optional[list]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    # Metadata
    metadata: Mapped[Optional[dict]] = mapped_column(
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
    partner = relationship("Partner", back_populates="spreads")
    readings = relationship("Reading", back_populates="spread")
    
    def __repr__(self) -> str:
        return f"<Spread(name='{self.name}', cards={self.card_count})>"
