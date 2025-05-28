"""
Partner endpoints for managing spiritual reading providers.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field

router = APIRouter()
security = HTTPBearer()


class PartnerResponse(BaseModel):
    """Partner response schema."""
    id: str
    slug: str
    name: str
    bio: Optional[str]
    photo_url: Optional[str]
    website: Optional[str]
    is_verified: bool
    revenue_share_percentage: float


class PersonaResponse(BaseModel):
    """Persona response schema."""
    id: str
    name: str
    title: Optional[str]
    bio: Optional[str]
    photo_url: Optional[str]
    specialties: Optional[List[str]]
    voice_style: Optional[str]
    tone: Optional[str]
    is_default: bool


@router.get("/", response_model=List[PartnerResponse])
async def list_partners():
    """
    List all active partners.
    
    Returns a list of all verified and active spiritual reading partners
    available on the platform.
    """
    # TODO: Implement partner listing from database
    return [
        PartnerResponse(
            id="default_partner_id",
            slug="metamystic",
            name="MetaMystic",
            bio="The default spiritual guide for MetaMystic platform",
            photo_url=None,
            website="https://metamystic.com",
            is_verified=True,
            revenue_share_percentage=0.0
        )
    ]


@router.get("/{partner_slug}", response_model=PartnerResponse)
async def get_partner(partner_slug: str):
    """
    Get partner details by slug.
    
    Returns detailed information about a specific partner including
    their bio, specialties, and available personas.
    """
    # TODO: Implement partner retrieval from database
    if partner_slug == "metamystic":
        return PartnerResponse(
            id="default_partner_id",
            slug="metamystic",
            name="MetaMystic",
            bio="The default spiritual guide for MetaMystic platform",
            photo_url=None,
            website="https://metamystic.com",
            is_verified=True,
            revenue_share_percentage=0.0
        )
    else:
        raise HTTPException(status_code=404, detail="Partner not found")


@router.get("/{partner_slug}/personas", response_model=List[PersonaResponse])
async def list_partner_personas(partner_slug: str):
    """
    List personas for a specific partner.
    
    Returns all available personas (spiritual guides) for the specified partner.
    """
    # TODO: Implement persona listing from database
    if partner_slug == "metamystic":
        return [
            PersonaResponse(
                id="default_persona_id",
                name="Sage",
                title="Spiritual Guide",
                bio="A wise and compassionate spiritual guide",
                photo_url=None,
                specialties=["General Guidance", "Life Path", "Spiritual Growth"],
                voice_style="wise",
                tone="compassionate",
                is_default=True
            )
        ]
    else:
        raise HTTPException(status_code=404, detail="Partner not found")


@router.get("/public")
async def get_public_partners():
    """
    Get public partner information for client applications.
    
    Returns minimal partner information suitable for public display
    in mobile and web applications.
    """
    # TODO: Implement public partner data
    return {
        "success": True,
        "data": {
            "partners": [
                {
                    "slug": "metamystic",
                    "name": "MetaMystic",
                    "description": "Default spiritual guide",
                    "photo_url": None,
                    "specialties": ["Astrology", "Tarot", "Numerology", "Chinese Zodiac"]
                }
            ],
            "default_partner": "metamystic"
        }
    }
