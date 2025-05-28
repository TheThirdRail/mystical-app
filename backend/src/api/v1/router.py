"""
Main API router for v1 endpoints.
"""

from fastapi import APIRouter

from .endpoints import (
    auth,
    readings,
    astro,
    numerology,
    zodiac,
    tarot,
    partners,
    admin,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(readings.router, prefix="/readings", tags=["readings"])
api_router.include_router(astro.router, prefix="/astro", tags=["astrology"])
api_router.include_router(numerology.router, prefix="/numerology", tags=["numerology"])
api_router.include_router(zodiac.router, prefix="/zodiac", tags=["chinese-zodiac"])
api_router.include_router(tarot.router, prefix="/tarot", tags=["tarot"])
api_router.include_router(partners.router, prefix="/partners", tags=["partners"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
