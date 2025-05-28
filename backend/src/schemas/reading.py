"""
Schemas for reading requests and responses.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class ReadingRequest(BaseModel):
    """Request schema for creating a reading."""
    
    # Birth information
    birth_date: datetime = Field(..., description="Date of birth")
    birth_time: Optional[str] = Field(None, description="Time of birth in HH:MM format")
    birth_location: Optional[str] = Field(None, description="Birth location name")
    birth_latitude: Optional[float] = Field(None, description="Birth latitude")
    birth_longitude: Optional[float] = Field(None, description="Birth longitude")
    
    # Personal information
    full_name: Optional[str] = Field(None, description="Full name for numerology")
    birth_name: Optional[str] = Field(None, description="Birth name if different")
    
    # Reading preferences
    partner_slug: Optional[str] = Field(None, description="Partner slug for custom persona")
    persona_id: Optional[str] = Field(None, description="Specific persona ID")
    deck_slug: Optional[str] = Field(None, description="Tarot deck to use")
    spread_slug: str = Field("three_card", description="Tarot spread to use")
    
    # User question
    question: Optional[str] = Field(None, description="User's specific question")
    
    # Options
    include_astrology: bool = Field(True, description="Include astrology in reading")
    include_numerology: bool = Field(True, description="Include numerology in reading")
    include_zodiac: bool = Field(True, description="Include Chinese zodiac in reading")
    include_tarot: bool = Field(True, description="Include tarot in reading")
    
    # Astrology options
    sidereal: bool = Field(False, description="Use sidereal astrology")
    ayanamsa: str = Field("LAHIRI", description="Ayanamsa system for sidereal")
    
    # Tarot options
    seed: Optional[int] = Field(None, description="Random seed for reproducible tarot draws")
    
    @validator("birth_time")
    def validate_birth_time(cls, v):
        """Validate birth time format."""
        if v is not None:
            try:
                hour, minute = map(int, v.split(":"))
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    raise ValueError("Invalid time")
            except (ValueError, AttributeError):
                raise ValueError("Birth time must be in HH:MM format")
        return v
    
    @validator("birth_latitude")
    def validate_latitude(cls, v):
        """Validate latitude range."""
        if v is not None and not (-90 <= v <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v
    
    @validator("birth_longitude")
    def validate_longitude(cls, v):
        """Validate longitude range."""
        if v is not None and not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v


class ReadingResponse(BaseModel):
    """Response schema for reading results."""
    
    id: str = Field(..., description="Reading ID")
    status: str = Field(..., description="Reading status")
    message: Optional[str] = Field(None, description="Status message")
    
    # Reading data (populated when completed)
    astrology_data: Optional[Dict[str, Any]] = Field(None, description="Astrology results")
    numerology_data: Optional[Dict[str, Any]] = Field(None, description="Numerology results")
    zodiac_data: Optional[Dict[str, Any]] = Field(None, description="Chinese zodiac results")
    tarot_data: Optional[Dict[str, Any]] = Field(None, description="Tarot results")
    
    # AI interpretation
    interpretation: Optional[str] = Field(None, description="AI-generated interpretation")
    
    # Metadata
    partner_slug: Optional[str] = Field(None, description="Partner used for reading")
    persona_name: Optional[str] = Field(None, description="Persona used for reading")
    deck_name: Optional[str] = Field(None, description="Tarot deck used")
    spread_name: Optional[str] = Field(None, description="Tarot spread used")
    
    # Processing info
    processing_time_ms: Optional[int] = Field(None, description="Processing time in milliseconds")
    llm_provider: Optional[str] = Field(None, description="LLM provider used")
    llm_model: Optional[str] = Field(None, description="LLM model used")
    
    # Timestamps
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    
    # Estimated completion time (for pending readings)
    estimated_completion_time: Optional[int] = Field(None, description="Estimated completion time in seconds")
    
    class Config:
        from_attributes = True


class ReadingPreview(BaseModel):
    """Preview schema for testing readings without saving."""
    
    astrology_data: Optional[Dict[str, Any]] = None
    numerology_data: Optional[Dict[str, Any]] = None
    zodiac_data: Optional[Dict[str, Any]] = None
    tarot_data: Optional[Dict[str, Any]] = None
    interpretation: Optional[str] = None
    processing_time_ms: Optional[int] = None
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
