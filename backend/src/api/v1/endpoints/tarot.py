"""
Tarot endpoints for card draws and interpretations.
"""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.core import tarot
from src.core.exceptions import CalculationError

router = APIRouter()


class TarotDrawRequest(BaseModel):
    """Request schema for tarot card draw."""
    
    spread_slug: str = Field("three_card", description="Spread to use for the reading")
    deck_slug: Optional[str] = Field(None, description="Deck to use (optional)")
    partner_slug: Optional[str] = Field(None, description="Partner slug for custom deck")
    seed: Optional[int] = Field(None, description="Random seed for reproducible draws")
    question: Optional[str] = Field(None, description="Question for the reading")


@router.post("/draw")
async def draw_tarot_cards(request: TarotDrawRequest):
    """
    Draw tarot cards for a reading.
    
    Draws cards according to the specified spread layout and returns
    positioned cards with their meanings and interpretations.
    """
    try:
        reading_data = tarot.draw_tarot_reading(
            spread_slug=request.spread_slug,
            deck_slug=request.deck_slug,
            partner_slug=request.partner_slug,
            seed=request.seed,
            question=request.question,
        )
        
        # Calculate reading themes
        themes = tarot.calculate_reading_themes(reading_data["cards"])
        reading_data["themes"] = themes
        
        return {
            "success": True,
            "data": reading_data
        }
        
    except CalculationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/spreads")
async def get_tarot_spreads():
    """
    Get available tarot spreads.
    
    Returns information about all available spreads including
    their layouts, positions, and usage instructions.
    """
    try:
        # Load spreads from default file
        import json
        from pathlib import Path
        
        spread_file = Path("data/spreads/default.json")
        with open(spread_file, "r", encoding="utf-8") as f:
            spreads_data = json.load(f)
        
        return {
            "success": True,
            "data": spreads_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/spreads/{spread_slug}")
async def get_tarot_spread(spread_slug: str):
    """
    Get specific tarot spread by slug.
    
    Returns detailed information about a specific spread including
    its layout, positions, and instructions.
    """
    try:
        spread = tarot.load_spread(spread_slug)
        
        return {
            "success": True,
            "data": spread
        }
        
    except CalculationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/decks")
async def get_tarot_decks():
    """
    Get available tarot decks.
    
    Returns information about all available decks including
    their metadata and card counts.
    """
    try:
        # For now, return the default deck info
        import json
        from pathlib import Path
        
        deck_file = Path("data/decks/rider_waite_smith.json")
        with open(deck_file, "r", encoding="utf-8") as f:
            deck_data = json.load(f)
        
        # Remove cards array for summary
        deck_summary = {k: v for k, v in deck_data.items() if k != "cards"}
        
        return {
            "success": True,
            "data": {
                "decks": [deck_summary],
                "default_deck": "rider_waite_smith"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/decks/{deck_slug}")
async def get_tarot_deck(deck_slug: str):
    """
    Get specific tarot deck by slug.
    
    Returns detailed information about a specific deck including
    all cards and their meanings.
    """
    try:
        deck = tarot.load_deck(deck_slug)
        
        return {
            "success": True,
            "data": deck
        }
        
    except CalculationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cards/major-arcana")
async def get_major_arcana():
    """
    Get all Major Arcana cards with their meanings.
    
    Returns the 22 Major Arcana cards with upright and reversed meanings,
    keywords, and symbolic interpretations.
    """
    try:
        deck = tarot.load_deck("rider_waite_smith")
        major_arcana = [card for card in deck["cards"] if card.get("arcana") == "major"]
        
        return {
            "success": True,
            "data": {
                "cards": major_arcana,
                "count": len(major_arcana),
                "description": "The Major Arcana represents major life themes, spiritual lessons, and karmic influences."
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cards/minor-arcana")
async def get_minor_arcana():
    """
    Get all Minor Arcana cards organized by suit.
    
    Returns the 56 Minor Arcana cards organized by suits (Cups, Wands, Swords, Pentacles)
    with their meanings and elemental associations.
    """
    try:
        deck = tarot.load_deck("rider_waite_smith")
        minor_arcana = [card for card in deck["cards"] if card.get("arcana") == "minor"]
        
        # Organize by suits
        suits = {
            "cups": [],
            "wands": [],
            "swords": [],
            "pentacles": []
        }
        
        for card in minor_arcana:
            suit = card.get("suit", "").lower()
            if suit in suits:
                suits[suit].append(card)
        
        return {
            "success": True,
            "data": {
                "suits": suits,
                "count": len(minor_arcana),
                "description": "The Minor Arcana represents day-to-day experiences, practical matters, and personal growth.",
                "suit_meanings": {
                    "cups": "Emotions, relationships, spirituality, intuition (Water element)",
                    "wands": "Creativity, passion, career, inspiration (Fire element)",
                    "swords": "Thoughts, communication, conflict, intellect (Air element)",
                    "pentacles": "Material matters, money, health, practical concerns (Earth element)"
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/interpret")
async def interpret_card(
    card_name: str,
    reversed: bool = False,
    position: Optional[str] = None
):
    """
    Get interpretation for a specific card.
    
    Returns detailed interpretation of a card including its meaning,
    keywords, and advice based on orientation and position.
    """
    try:
        deck = tarot.load_deck("rider_waite_smith")
        
        # Find the card
        card = None
        for c in deck["cards"]:
            if c["name"].lower() == card_name.lower():
                card = c
                break
        
        if not card:
            raise HTTPException(status_code=404, detail=f"Card '{card_name}' not found")
        
        # Add reversed flag
        card["reversed"] = reversed
        
        # Create position info if provided
        position_info = {"name": position} if position else None
        
        # Get interpretation
        interpretation = tarot.interpret_card(card, position_info)
        
        return {
            "success": True,
            "data": interpretation
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
