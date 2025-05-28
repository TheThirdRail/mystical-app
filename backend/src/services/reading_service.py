"""
Reading service for orchestrating spiritual consultations.
"""

import time
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.reading import Reading, ReadingStatus
from src.models.partner import Partner
from src.models.persona import Persona
from src.models.deck import Deck
from src.models.spread import Spread
from src.schemas.reading import ReadingRequest, ReadingPreview
from src.core import astro, numerology, zodiac, tarot
from src.services.ai import get_llm_provider
from src.core.config import settings
from src.core.exceptions import MetaMysticException, CalculationError, LLMProviderError


class ReadingService:
    """Service for managing spiritual readings."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_reading(self, request: ReadingRequest) -> Reading:
        """Create a new reading record."""
        # Get partner and persona
        partner = await self._get_partner(request.partner_slug)
        persona = await self._get_persona(request.persona_id, partner)
        
        # Get deck and spread
        deck = await self._get_deck(request.deck_slug, partner)
        spread = await self._get_spread(request.spread_slug, partner)
        
        # Create reading record
        reading = Reading(
            partner_id=partner.id,
            persona_id=persona.id if persona else None,
            deck_id=deck.id,
            spread_id=spread.id,
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            birth_location=request.birth_location,
            birth_latitude=request.birth_latitude,
            birth_longitude=request.birth_longitude,
            question=request.question,
            status=ReadingStatus.PENDING,
        )
        
        self.db.add(reading)
        await self.db.commit()
        await self.db.refresh(reading)
        
        return reading
    
    async def process_reading(self, reading_id: str) -> Reading:
        """Process a reading by performing all calculations and AI interpretation."""
        start_time = time.time()
        
        # Get reading
        reading = await self.get_reading(reading_id)
        if not reading:
            raise MetaMysticException("Reading not found", 404)
        
        try:
            # Update status to processing
            reading.status = ReadingStatus.PROCESSING
            await self.db.commit()
            
            # Perform calculations
            calculations = await self._perform_calculations(reading)
            
            # Get AI interpretation
            interpretation = await self._get_ai_interpretation(reading, calculations)
            
            # Update reading with results
            reading.astrology_data = calculations.get("astrology")
            reading.numerology_data = calculations.get("numerology")
            reading.zodiac_data = calculations.get("zodiac")
            reading.tarot_data = calculations.get("tarot")
            reading.interpretation = interpretation["content"]
            reading.llm_provider = interpretation["provider"]
            reading.llm_model = interpretation["model"]
            reading.processing_time_ms = int((time.time() - start_time) * 1000)
            reading.status = ReadingStatus.COMPLETED
            
            await self.db.commit()
            
            return reading
            
        except Exception as e:
            # Mark as failed
            reading.status = ReadingStatus.FAILED
            await self.db.commit()
            raise
    
    async def preview_reading(self, request: ReadingRequest) -> ReadingPreview:
        """Preview a reading without saving to database."""
        start_time = time.time()
        
        # Create temporary reading object for calculations
        temp_reading = Reading(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            birth_location=request.birth_location,
            birth_latitude=request.birth_latitude,
            birth_longitude=request.birth_longitude,
            question=request.question,
        )
        
        # Perform calculations
        calculations = await self._perform_calculations(temp_reading, request)
        
        # Get AI interpretation
        interpretation = await self._get_ai_interpretation(temp_reading, calculations, request)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return ReadingPreview(
            astrology_data=calculations.get("astrology"),
            numerology_data=calculations.get("numerology"),
            zodiac_data=calculations.get("zodiac"),
            tarot_data=calculations.get("tarot"),
            interpretation=interpretation["content"],
            processing_time_ms=processing_time,
            llm_provider=interpretation["provider"],
            llm_model=interpretation["model"],
        )
    
    async def get_reading(self, reading_id: str) -> Optional[Reading]:
        """Get reading by ID."""
        result = await self.db.execute(
            select(Reading).where(Reading.id == reading_id)
        )
        return result.scalar_one_or_none()
    
    async def _perform_calculations(
        self, 
        reading: Reading, 
        request: Optional[ReadingRequest] = None
    ) -> Dict[str, Any]:
        """Perform all spiritual calculations."""
        calculations = {}
        
        # Astrology calculation
        if not request or request.include_astrology:
            if reading.birth_date and reading.birth_time and reading.birth_latitude and reading.birth_longitude:
                try:
                    astro_data = astro.calculate_birth_chart(
                        birth_date=reading.birth_date,
                        birth_time=reading.birth_time,
                        birth_location=reading.birth_location or "Unknown",
                        latitude=float(reading.birth_latitude),
                        longitude=float(reading.birth_longitude),
                        sidereal=request.sidereal if request else False,
                        ayanamsa=request.ayanamsa if request else "LAHIRI",
                    )
                    calculations["astrology"] = astro_data
                except Exception as e:
                    print(f"Astrology calculation failed: {e}")
        
        # Numerology calculation
        if not request or request.include_numerology:
            if reading.birth_date:
                try:
                    full_name = getattr(request, 'full_name', None) if request else "Unknown"
                    birth_name = getattr(request, 'birth_name', None) if request else None
                    
                    if full_name:
                        num_data = numerology.calculate_numerology_profile(
                            birth_date=reading.birth_date,
                            full_name=full_name,
                            birth_name=birth_name,
                        )
                        calculations["numerology"] = num_data
                except Exception as e:
                    print(f"Numerology calculation failed: {e}")
        
        # Chinese zodiac calculation
        if not request or request.include_zodiac:
            if reading.birth_date:
                try:
                    zodiac_data = zodiac.calculate_chinese_zodiac(reading.birth_date)
                    calculations["zodiac"] = zodiac_data
                except Exception as e:
                    print(f"Zodiac calculation failed: {e}")
        
        # Tarot calculation
        if not request or request.include_tarot:
            try:
                spread_slug = request.spread_slug if request else "three_card"
                deck_slug = request.deck_slug if request else None
                partner_slug = request.partner_slug if request else None
                seed = request.seed if request else None
                
                tarot_data = tarot.draw_tarot_reading(
                    spread_slug=spread_slug,
                    deck_slug=deck_slug,
                    partner_slug=partner_slug,
                    seed=seed,
                    question=reading.question,
                )
                calculations["tarot"] = tarot_data
            except Exception as e:
                print(f"Tarot calculation failed: {e}")
        
        return calculations
    
    async def _get_ai_interpretation(
        self, 
        reading: Reading, 
        calculations: Dict[str, Any],
        request: Optional[ReadingRequest] = None
    ) -> Dict[str, Any]:
        """Get AI interpretation of the reading."""
        try:
            # Get LLM provider
            provider = get_llm_provider()
            
            # Get partner and persona info for prompt customization
            partner_prompt_stub = None
            persona_config = None
            
            if hasattr(reading, 'partner') and reading.partner:
                partner_prompt_stub = reading.partner.prompt_stub
            
            if hasattr(reading, 'persona') and reading.persona:
                persona_config = {
                    "voice_style": reading.persona.voice_style,
                    "tone": reading.persona.tone,
                    "prompt_prefix": reading.persona.prompt_prefix,
                    "prompt_suffix": reading.persona.prompt_suffix,
                }
            
            # Format prompt
            prompt = provider.format_reading_prompt(
                astro_data=calculations.get("astrology"),
                numerology_data=calculations.get("numerology"),
                zodiac_data=calculations.get("zodiac"),
                tarot_data=calculations.get("tarot"),
                question=reading.question,
                partner_prompt_stub=partner_prompt_stub,
                persona_config=persona_config,
            )
            
            # Generate interpretation
            response = await provider.generate_response(prompt)
            
            return response
            
        except Exception as e:
            raise LLMProviderError("unknown", f"Failed to generate interpretation: {str(e)}")
    
    async def _get_partner(self, partner_slug: Optional[str]) -> Partner:
        """Get partner by slug or default."""
        if partner_slug:
            result = await self.db.execute(
                select(Partner).where(Partner.slug == partner_slug)
            )
            partner = result.scalar_one_or_none()
            if partner:
                return partner
        
        # Get default partner
        result = await self.db.execute(
            select(Partner).where(Partner.slug == settings.DEFAULT_PARTNER_SLUG)
        )
        partner = result.scalar_one_or_none()
        
        if not partner:
            raise MetaMysticException("No default partner found", 500)
        
        return partner
    
    async def _get_persona(self, persona_id: Optional[str], partner: Partner) -> Optional[Persona]:
        """Get persona by ID or partner's default."""
        if persona_id:
            result = await self.db.execute(
                select(Persona).where(Persona.id == persona_id)
            )
            return result.scalar_one_or_none()
        
        # Get partner's default persona
        result = await self.db.execute(
            select(Persona).where(
                Persona.partner_id == partner.id,
                Persona.is_default == True
            )
        )
        return result.scalar_one_or_none()
    
    async def _get_deck(self, deck_slug: Optional[str], partner: Partner) -> Deck:
        """Get deck by slug or default."""
        if deck_slug:
            result = await self.db.execute(
                select(Deck).where(Deck.slug == deck_slug)
            )
            deck = result.scalar_one_or_none()
            if deck:
                return deck
        
        # Get default deck
        result = await self.db.execute(
            select(Deck).where(Deck.slug == settings.DEFAULT_TAROT_DECK)
        )
        deck = result.scalar_one_or_none()
        
        if not deck:
            raise MetaMysticException("No default deck found", 500)
        
        return deck
    
    async def _get_spread(self, spread_slug: str, partner: Partner) -> Spread:
        """Get spread by slug."""
        result = await self.db.execute(
            select(Spread).where(Spread.slug == spread_slug)
        )
        spread = result.scalar_one_or_none()
        
        if not spread:
            raise MetaMysticException(f"Spread '{spread_slug}' not found", 404)
        
        return spread
