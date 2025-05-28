"""
Payment model for revenue tracking.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import String, ForeignKey, JSON, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class PaymentStatus(str, Enum):
    """Payment status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentMethod(str, Enum):
    """Payment method."""
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    APPLE_PAY = "apple_pay"
    GOOGLE_PAY = "google_pay"
    STRIPE = "stripe"


class Payment(BaseModel):
    """Payment model for revenue tracking."""
    
    __tablename__ = "payments"
    
    reading_id: Mapped[str] = mapped_column(
        ForeignKey("readings.id"),
        nullable=False,
        index=True,
    )
    
    partner_id: Mapped[str] = mapped_column(
        ForeignKey("partners.id"),
        nullable=False,
        index=True,
    )
    
    user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )
    
    # Payment details
    amount: Mapped[float] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
    )
    
    currency: Mapped[str] = mapped_column(
        String(3),
        default="USD",
        nullable=False,
    )
    
    status: Mapped[PaymentStatus] = mapped_column(
        default=PaymentStatus.PENDING,
        nullable=False,
    )
    
    method: Mapped[Optional[PaymentMethod]] = mapped_column(
        nullable=True,
    )
    
    # Revenue split
    partner_amount: Mapped[float] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
    )
    
    platform_amount: Mapped[float] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
    )
    
    partner_percentage: Mapped[float] = mapped_column(
        Numeric(precision=5, scale=2),
        nullable=False,
    )
    
    # External payment processor data
    external_payment_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    
    processor: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    
    processor_data: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    # Timestamps
    processed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    refunded_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Metadata
    metadata: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    # Relationships
    reading = relationship("Reading", back_populates="payment")
    partner = relationship("Partner", back_populates="payments")
    user = relationship("User")
    
    def __repr__(self) -> str:
        return f"<Payment(id='{self.id}', amount={self.amount}, status='{self.status}')>"
