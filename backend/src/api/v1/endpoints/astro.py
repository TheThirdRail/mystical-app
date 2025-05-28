"""
Astrology endpoints for birth chart calculations.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, validator

from src.core import astro
from src.core.exceptions import CalculationError

router = APIRouter()


class BirthChartRequest(BaseModel):
    """Request schema for birth chart calculation."""
    
    birth_date: datetime = Field(..., description="Date of birth")
    birth_time: str = Field(..., description="Time of birth in HH:MM format")
    birth_location: str = Field(..., description="Birth location name")
    latitude: float = Field(..., description="Birth latitude")
    longitude: float = Field(..., description="Birth longitude")
    sidereal: bool = Field(False, description="Use sidereal astrology")
    ayanamsa: str = Field("LAHIRI", description="Ayanamsa system for sidereal")
    
    @validator("birth_time")
    def validate_birth_time(cls, v):
        """Validate birth time format."""
        try:
            hour, minute = map(int, v.split(":"))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Invalid time")
        except (ValueError, AttributeError):
            raise ValueError("Birth time must be in HH:MM format")
        return v
    
    @validator("latitude")
    def validate_latitude(cls, v):
        """Validate latitude range."""
        if not (-90 <= v <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v
    
    @validator("longitude")
    def validate_longitude(cls, v):
        """Validate longitude range."""
        if not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v


class CompatibilityRequest(BaseModel):
    """Request schema for compatibility calculation."""
    
    person1: BirthChartRequest = Field(..., description="First person's birth data")
    person2: BirthChartRequest = Field(..., description="Second person's birth data")


@router.post("/chart")
async def calculate_birth_chart(request: BirthChartRequest):
    """
    Calculate birth chart for given birth data.
    
    Returns both tropical and sidereal calculations with planetary positions,
    houses, aspects, and elemental analysis.
    """
    try:
        chart_data = astro.calculate_birth_chart(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            birth_location=request.birth_location,
            latitude=request.latitude,
            longitude=request.longitude,
            ayanamsa=request.ayanamsa,
            sidereal=request.sidereal,
        )
        
        return {
            "success": True,
            "data": chart_data,
            "calculation_type": "sidereal" if request.sidereal else "tropical",
            "ayanamsa": request.ayanamsa if request.sidereal else None,
        }
        
    except CalculationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compatibility")
async def calculate_compatibility(request: CompatibilityRequest):
    """
    Calculate compatibility between two birth charts.
    
    Analyzes synastry aspects, element compatibility, and overall harmony
    between two people based on their birth data.
    """
    try:
        # Calculate both charts
        chart1 = astro.calculate_birth_chart(
            birth_date=request.person1.birth_date,
            birth_time=request.person1.birth_time,
            birth_location=request.person1.birth_location,
            latitude=request.person1.latitude,
            longitude=request.person1.longitude,
            ayanamsa=request.person1.ayanamsa,
            sidereal=request.person1.sidereal,
        )
        
        chart2 = astro.calculate_birth_chart(
            birth_date=request.person2.birth_date,
            birth_time=request.person2.birth_time,
            birth_location=request.person2.birth_location,
            latitude=request.person2.latitude,
            longitude=request.person2.longitude,
            ayanamsa=request.person2.ayanamsa,
            sidereal=request.person2.sidereal,
        )
        
        # Calculate compatibility
        compatibility = astro.calculate_compatibility(chart1, chart2)
        
        return {
            "success": True,
            "data": {
                "person1_chart": chart1,
                "person2_chart": chart2,
                "compatibility": compatibility,
            }
        }
        
    except CalculationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/signs")
async def get_zodiac_signs():
    """
    Get information about all zodiac signs.
    
    Returns details about each sign including element, modality,
    ruling planet, and basic characteristics.
    """
    signs = [
        {
            "name": "Aries",
            "symbol": "♈",
            "element": "Fire",
            "modality": "Cardinal",
            "ruling_planet": "Mars",
            "dates": "March 21 - April 19",
            "keywords": ["Leadership", "Initiative", "Courage", "Independence"]
        },
        {
            "name": "Taurus",
            "symbol": "♉",
            "element": "Earth",
            "modality": "Fixed",
            "ruling_planet": "Venus",
            "dates": "April 20 - May 20",
            "keywords": ["Stability", "Sensuality", "Determination", "Practicality"]
        },
        {
            "name": "Gemini",
            "symbol": "♊",
            "element": "Air",
            "modality": "Mutable",
            "ruling_planet": "Mercury",
            "dates": "May 21 - June 20",
            "keywords": ["Communication", "Curiosity", "Adaptability", "Intelligence"]
        },
        {
            "name": "Cancer",
            "symbol": "♋",
            "element": "Water",
            "modality": "Cardinal",
            "ruling_planet": "Moon",
            "dates": "June 21 - July 22",
            "keywords": ["Nurturing", "Intuition", "Emotion", "Protection"]
        },
        {
            "name": "Leo",
            "symbol": "♌",
            "element": "Fire",
            "modality": "Fixed",
            "ruling_planet": "Sun",
            "dates": "July 23 - August 22",
            "keywords": ["Creativity", "Leadership", "Confidence", "Generosity"]
        },
        {
            "name": "Virgo",
            "symbol": "♍",
            "element": "Earth",
            "modality": "Mutable",
            "ruling_planet": "Mercury",
            "dates": "August 23 - September 22",
            "keywords": ["Analysis", "Service", "Perfection", "Health"]
        },
        {
            "name": "Libra",
            "symbol": "♎",
            "element": "Air",
            "modality": "Cardinal",
            "ruling_planet": "Venus",
            "dates": "September 23 - October 22",
            "keywords": ["Balance", "Harmony", "Justice", "Relationships"]
        },
        {
            "name": "Scorpio",
            "symbol": "♏",
            "element": "Water",
            "modality": "Fixed",
            "ruling_planet": "Pluto",
            "dates": "October 23 - November 21",
            "keywords": ["Transformation", "Intensity", "Mystery", "Power"]
        },
        {
            "name": "Sagittarius",
            "symbol": "♐",
            "element": "Fire",
            "modality": "Mutable",
            "ruling_planet": "Jupiter",
            "dates": "November 22 - December 21",
            "keywords": ["Adventure", "Philosophy", "Freedom", "Optimism"]
        },
        {
            "name": "Capricorn",
            "symbol": "♑",
            "element": "Earth",
            "modality": "Cardinal",
            "ruling_planet": "Saturn",
            "dates": "December 22 - January 19",
            "keywords": ["Ambition", "Discipline", "Structure", "Achievement"]
        },
        {
            "name": "Aquarius",
            "symbol": "♒",
            "element": "Air",
            "modality": "Fixed",
            "ruling_planet": "Uranus",
            "dates": "January 20 - February 18",
            "keywords": ["Innovation", "Independence", "Humanitarianism", "Originality"]
        },
        {
            "name": "Pisces",
            "symbol": "♓",
            "element": "Water",
            "modality": "Mutable",
            "ruling_planet": "Neptune",
            "dates": "February 19 - March 20",
            "keywords": ["Compassion", "Intuition", "Spirituality", "Imagination"]
        }
    ]
    
    return {
        "success": True,
        "data": {
            "signs": signs,
            "elements": {
                "Fire": ["Aries", "Leo", "Sagittarius"],
                "Earth": ["Taurus", "Virgo", "Capricorn"],
                "Air": ["Gemini", "Libra", "Aquarius"],
                "Water": ["Cancer", "Scorpio", "Pisces"]
            },
            "modalities": {
                "Cardinal": ["Aries", "Cancer", "Libra", "Capricorn"],
                "Fixed": ["Taurus", "Leo", "Scorpio", "Aquarius"],
                "Mutable": ["Gemini", "Virgo", "Sagittarius", "Pisces"]
            }
        }
    }
