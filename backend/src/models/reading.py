"""
Reading model for spiritual consultations.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import String, Text, Boolean, ForeignKey, JSON, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class ReadingStatus(str, Enum):
    """Reading status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Reading(BaseModel):
    """Reading model."""
    
    __tablename__ = "readings"
    
    user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )
    
    partner_id: Mapped[str] = mapped_column(
        ForeignKey("partners.id"),
        nullable=False,
        index=True,
    )
    
    persona_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("personas.id"),
        nullable=True,
        index=True,
    )
    
    deck_id: Mapped[str] = mapped_column(
        ForeignKey("decks.id"),
        nullable=False,
        index=True,
    )
    
    spread_id: Mapped[str] = mapped_column(
        ForeignKey("spreads.id"),
        nullable=False,
        index=True,
    )
    
    # Reading metadata
    session_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    
    status: Mapped[ReadingStatus] = mapped_column(
        default=ReadingStatus.PENDING,
        nullable=False,
    )
    
    # User input
    birth_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    birth_time: Mapped[Optional[str]] = mapped_column(
        String(10),  # HH:MM format
        nullable=True,
    )
    
    birth_location: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    birth_latitude: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=10, scale=7),
        nullable=True,
    )
    
    birth_longitude: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=10, scale=7),
        nullable=True,
    )
    
    question: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Reading results
    astrology_data: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    numerology_data: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    zodiac_data: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    tarot_data: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    # AI interpretation
    interpretation: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Processing metadata
    processing_time_ms: Mapped[Optional[int]] = mapped_column(
        nullable=True,
    )
    
    llm_provider: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    
    llm_model: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    
    # Pricing
    price: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=True,
    )
    
    currency: Mapped[str] = mapped_column(
        String(3),
        default="USD",
        nullable=False,
    )
    
    # Relationships
    user = relationship("User", back_populates="readings")
    partner = relationship("Partner", back_populates="readings")
    persona = relationship("Persona", back_populates="readings")
    deck = relationship("Deck", back_populates="readings")
    spread = relationship("Spread", back_populates="readings")
    payment = relationship("Payment", back_populates="reading", uselist=False)
    
    def __repr__(self) -> str:
        return f"<Reading(id='{self.id}', status='{self.status}', partner='{self.partner.slug if self.partner else None}')>"
