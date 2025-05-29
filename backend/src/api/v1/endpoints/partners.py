"""
Partner endpoints for managing spiritual reading providers.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.database import get_db
from src.core.exceptions import NotFoundError, AuthorizationError
from src.models.partner import Partner
from src.models.persona import Persona
from src.models.user import User
from src.api.v1.endpoints.auth import get_current_user

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

    class Config:
        from_attributes = True


class PartnerCreateRequest(BaseModel):
    """Partner creation request schema."""
    slug: str = Field(..., description="Unique partner slug")
    name: str = Field(..., description="Partner name")
    email: EmailStr = Field(..., description="Partner email")
    bio: Optional[str] = Field(None, description="Partner bio")
    website: Optional[str] = Field(None, description="Partner website")
    revenue_share_percentage: float = Field(70.0, description="Revenue share percentage")


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

    class Config:
        from_attributes = True


class PersonaCreateRequest(BaseModel):
    """Persona creation request schema."""
    name: str = Field(..., description="Persona name")
    title: Optional[str] = Field(None, description="Persona title")
    bio: Optional[str] = Field(None, description="Persona bio")
    specialties: Optional[List[str]] = Field(None, description="Persona specialties")
    voice_style: Optional[str] = Field(None, description="AI voice style")
    tone: Optional[str] = Field(None, description="AI tone")
    prompt_prefix: Optional[str] = Field(None, description="Prompt prefix")
    prompt_suffix: Optional[str] = Field(None, description="Prompt suffix")


@router.get("/", response_model=List[PartnerResponse])
async def list_partners(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    List all active partners.

    Returns a list of all verified and active spiritual reading partners
    available on the platform.
    """
    stmt = select(Partner).where(
        Partner.is_active == True
    ).offset(skip).limit(limit)

    result = await db.execute(stmt)
    partners = result.scalars().all()

    return [PartnerResponse.from_orm(partner) for partner in partners]


@router.post("/", response_model=PartnerResponse)
async def create_partner(
    request: PartnerCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new partner.

    Only authenticated users can create partners.
    """
    # Check if slug already exists
    stmt = select(Partner).where(Partner.slug == request.slug)
    result = await db.execute(stmt)
    existing_partner = result.scalar_one_or_none()

    if existing_partner:
        raise HTTPException(
            status_code=400,
            detail="Partner slug already exists"
        )

    # Create new partner
    partner = Partner(
        user_id=current_user.id,
        slug=request.slug,
        name=request.name,
        email=request.email,
        bio=request.bio,
        website=request.website,
        revenue_share_percentage=request.revenue_share_percentage,
        is_active=True,
        is_verified=False  # Requires admin verification
    )

    db.add(partner)
    await db.commit()
    await db.refresh(partner)

    return PartnerResponse.from_orm(partner)


@router.get("/{partner_slug}", response_model=PartnerResponse)
async def get_partner(
    partner_slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get partner by slug.
    """
    stmt = select(Partner).where(Partner.slug == partner_slug)
    result = await db.execute(stmt)
    partner = result.scalar_one_or_none()

    if not partner:
        raise HTTPException(
            status_code=404,
            detail="Partner not found"
        )

    return PartnerResponse.from_orm(partner)


# Note: get_partner endpoint already implemented above


@router.get("/{partner_slug}/personas", response_model=List[PersonaResponse])
async def list_partner_personas(
    partner_slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    List personas for a specific partner.

    Returns all available personas (spiritual guides) for the specified partner.
    """
    # First get the partner
    stmt = select(Partner).where(Partner.slug == partner_slug)
    result = await db.execute(stmt)
    partner = result.scalar_one_or_none()

    if not partner:
        raise HTTPException(
            status_code=404,
            detail="Partner not found"
        )

    # Get partner's personas
    stmt = select(Persona).where(
        Persona.partner_id == partner.id,
        Persona.is_active == True
    )
    result = await db.execute(stmt)
    personas = result.scalars().all()

    return [PersonaResponse.from_orm(persona) for persona in personas]


@router.post("/{partner_slug}/personas", response_model=PersonaResponse)
async def create_persona(
    partner_slug: str,
    request: PersonaCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new persona for a partner.

    Only the partner owner can create personas.
    """
    # Get the partner
    stmt = select(Partner).where(Partner.slug == partner_slug)
    result = await db.execute(stmt)
    partner = result.scalar_one_or_none()

    if not partner:
        raise HTTPException(
            status_code=404,
            detail="Partner not found"
        )

    # Check if user owns this partner
    if partner.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to create personas for this partner"
        )

    # Create new persona
    persona = Persona(
        partner_id=partner.id,
        name=request.name,
        title=request.title,
        bio=request.bio,
        specialties=request.specialties,
        voice_style=request.voice_style,
        tone=request.tone,
        prompt_prefix=request.prompt_prefix,
        prompt_suffix=request.prompt_suffix,
        is_active=True,
        is_default=False
    )

    db.add(persona)
    await db.commit()
    await db.refresh(persona)

    return PersonaResponse.from_orm(persona)


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
