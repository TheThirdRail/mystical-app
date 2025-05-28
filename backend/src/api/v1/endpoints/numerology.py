"""
Numerology endpoints for number calculations.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.core import numerology
from src.core.exceptions import CalculationError

router = APIRouter()


class NumerologyRequest(BaseModel):
    """Request schema for numerology calculation."""
    
    birth_date: datetime = Field(..., description="Date of birth")
    full_name: str = Field(..., description="Full name for calculations")
    birth_name: Optional[str] = Field(None, description="Birth name if different from current name")


@router.post("/profile")
async def calculate_numerology_profile(request: NumerologyRequest):
    """
    Calculate complete numerology profile.
    
    Returns core numbers (Life Path, Expression, Soul Urge, Personality, Birthday),
    additional numbers (Maturity, Balance, Karmic Debt), and current cycles.
    """
    try:
        profile = numerology.calculate_numerology_profile(
            birth_date=request.birth_date,
            full_name=request.full_name,
            birth_name=request.birth_name,
        )
        
        return {
            "success": True,
            "data": profile
        }
        
    except CalculationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/life-path")
async def calculate_life_path(birth_date: datetime):
    """
    Calculate Life Path number from birth date.
    
    The Life Path number is the most important number in numerology,
    representing your life's purpose and the path you're meant to walk.
    """
    try:
        life_path = numerology.calculate_life_path_number(birth_date)
        
        return {
            "success": True,
            "data": life_path
        }
        
    except CalculationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/expression")
async def calculate_expression(full_name: str):
    """
    Calculate Expression number from full name.
    
    The Expression number reveals your talents, abilities, and goals.
    It represents what you're meant to accomplish in this lifetime.
    """
    try:
        expression = numerology.calculate_expression_number(full_name)
        
        return {
            "success": True,
            "data": expression
        }
        
    except CalculationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/soul-urge")
async def calculate_soul_urge(full_name: str):
    """
    Calculate Soul Urge number from vowels in name.
    
    The Soul Urge number represents your inner desires, motivations,
    and what truly drives you from within.
    """
    try:
        soul_urge = numerology.calculate_soul_urge_number(full_name)
        
        return {
            "success": True,
            "data": soul_urge
        }
        
    except CalculationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/personality")
async def calculate_personality(full_name: str):
    """
    Calculate Personality number from consonants in name.
    
    The Personality number represents how others see you and the
    impression you make on the world.
    """
    try:
        personality = numerology.calculate_personality_number(full_name)
        
        return {
            "success": True,
            "data": personality
        }
        
    except CalculationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/personal-year")
async def calculate_personal_year(birth_date: datetime):
    """
    Calculate Personal Year number for current year.
    
    The Personal Year number reveals the theme and energy
    of your current year cycle.
    """
    try:
        personal_year = numerology.calculate_personal_year(birth_date)
        
        return {
            "success": True,
            "data": {
                "personal_year": personal_year,
                "meaning": numerology.get_life_path_meaning(personal_year),
                "year": datetime.now().year
            }
        }
        
    except CalculationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/meanings")
async def get_number_meanings():
    """
    Get meanings for all numerology numbers 1-9 and master numbers 11, 22, 33.
    
    Returns comprehensive descriptions of what each number represents
    in numerological interpretation.
    """
    meanings = {
        "1": {
            "keywords": ["Leadership", "Independence", "Initiative", "Originality"],
            "description": "The leader and pioneer. Natural born leaders who are independent, original, and ambitious.",
            "strengths": ["Leadership", "Independence", "Determination", "Innovation"],
            "challenges": ["Selfishness", "Impatience", "Arrogance", "Stubbornness"]
        },
        "2": {
            "keywords": ["Cooperation", "Harmony", "Diplomacy", "Partnership"],
            "description": "The peacemaker and diplomat. Naturally cooperative, sensitive, and diplomatic.",
            "strengths": ["Cooperation", "Sensitivity", "Diplomacy", "Patience"],
            "challenges": ["Over-sensitivity", "Indecision", "Dependency", "Passivity"]
        },
        "3": {
            "keywords": ["Creativity", "Communication", "Expression", "Joy"],
            "description": "The creative communicator. Naturally artistic, expressive, and optimistic.",
            "strengths": ["Creativity", "Communication", "Optimism", "Inspiration"],
            "challenges": ["Scattered energy", "Superficiality", "Mood swings", "Criticism"]
        },
        "4": {
            "keywords": ["Stability", "Hard work", "Organization", "Practicality"],
            "description": "The builder and organizer. Naturally practical, reliable, and hardworking.",
            "strengths": ["Reliability", "Organization", "Hard work", "Loyalty"],
            "challenges": ["Rigidity", "Stubbornness", "Narrow-mindedness", "Dullness"]
        },
        "5": {
            "keywords": ["Freedom", "Adventure", "Change", "Versatility"],
            "description": "The adventurer and free spirit. Naturally curious, versatile, and freedom-loving.",
            "strengths": ["Versatility", "Curiosity", "Adventure", "Progressive thinking"],
            "challenges": ["Restlessness", "Irresponsibility", "Inconsistency", "Addiction"]
        },
        "6": {
            "keywords": ["Nurturing", "Responsibility", "Healing", "Service"],
            "description": "The nurturer and healer. Naturally caring, responsible, and service-oriented.",
            "strengths": ["Nurturing", "Responsibility", "Compassion", "Healing"],
            "challenges": ["Interference", "Worry", "Self-righteousness", "Martyrdom"]
        },
        "7": {
            "keywords": ["Spirituality", "Analysis", "Introspection", "Wisdom"],
            "description": "The seeker and mystic. Naturally spiritual, analytical, and introspective.",
            "strengths": ["Spirituality", "Analysis", "Intuition", "Wisdom"],
            "challenges": ["Isolation", "Skepticism", "Coldness", "Pessimism"]
        },
        "8": {
            "keywords": ["Material success", "Authority", "Achievement", "Power"],
            "description": "The achiever and executive. Naturally ambitious, organized, and success-oriented.",
            "strengths": ["Leadership", "Organization", "Ambition", "Material success"],
            "challenges": ["Materialism", "Workaholism", "Impatience", "Stress"]
        },
        "9": {
            "keywords": ["Humanitarianism", "Compassion", "Generosity", "Wisdom"],
            "description": "The humanitarian and teacher. Naturally compassionate, generous, and wise.",
            "strengths": ["Compassion", "Generosity", "Wisdom", "Universal love"],
            "challenges": ["Emotional volatility", "Impracticality", "Moodiness", "Resentment"]
        },
        "11": {
            "keywords": ["Intuition", "Inspiration", "Enlightenment", "Spiritual insight"],
            "description": "The spiritual messenger. Master number representing intuition, inspiration, and enlightenment.",
            "strengths": ["Intuition", "Inspiration", "Spiritual insight", "Idealism"],
            "challenges": ["Nervous tension", "Impracticality", "Fanaticism", "Confusion"]
        },
        "22": {
            "keywords": ["Master builder", "Practical idealism", "Large-scale achievement"],
            "description": "The master builder. Master number representing the ability to turn dreams into reality.",
            "strengths": ["Practical idealism", "Large-scale thinking", "Leadership", "Achievement"],
            "challenges": ["Pressure", "Self-doubt", "Nervous tension", "Extremes"]
        },
        "33": {
            "keywords": ["Master teacher", "Compassion", "Healing", "Service"],
            "description": "The master teacher. Master number representing compassionate service and healing.",
            "strengths": ["Compassion", "Healing", "Teaching", "Service"],
            "challenges": ["Emotional burden", "Martyrdom", "Criticism", "Perfectionism"]
        }
    }
    
    return {
        "success": True,
        "data": {
            "meanings": meanings,
            "master_numbers": ["11", "22", "33"],
            "core_numbers": ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        }
    }
