"""
Deck and Card models for tarot readings.
"""

from typing import Optional

from sqlalchemy import String, Text, Boolean, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Deck(BaseModel):
    """Tarot deck model."""
    
    __tablename__ = "decks"
    
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
    
    author: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    publisher: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    year_published: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    # Deck configuration
    card_count: Mapped[int] = mapped_column(
        Integer,
        default=78,
        nullable=False,
    )
    
    has_major_arcana: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    has_minor_arcana: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
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
    partner = relationship("Partner", back_populates="decks")
    cards = relationship("Card", back_populates="deck", cascade="all, delete-orphan")
    readings = relationship("Reading", back_populates="deck")
    
    def __repr__(self) -> str:
        return f"<Deck(name='{self.name}', slug='{self.slug}')>"


class Card(BaseModel):
    """Tarot card model."""
    
    __tablename__ = "cards"
    
    deck_id: Mapped[str] = mapped_column(
        ForeignKey("decks.id"),
        nullable=False,
        index=True,
    )
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    number: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    suit: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    
    arcana: Mapped[str] = mapped_column(
        String(20),
        nullable=False,  # 'major' or 'minor'
    )
    
    # Card meanings
    upright_meaning: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    reversed_meaning: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    keywords_upright: Mapped[Optional[list]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    keywords_reversed: Mapped[Optional[list]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    # Images
    image_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    
    image_url_reversed: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    
    # Metadata
    metadata: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    # Relationships
    deck = relationship("Deck", back_populates="cards")
    
    def __repr__(self) -> str:
        return f"<Card(name='{self.name}', deck='{self.deck.name if self.deck else None}')>"
