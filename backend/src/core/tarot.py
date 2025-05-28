"""
Tarot calculation module.

Provides tarot card drawing, spread layouts, and card interpretation functionality.
"""

import json
import random
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from src.core.config import settings
from src.core.exceptions import CalculationError


def draw_tarot_reading(
    spread_slug: str,
    deck_slug: str = None,
    partner_slug: str = None,
    seed: Optional[int] = None,
    question: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Draw tarot cards for a reading.
    
    Args:
        spread_slug: Slug of the spread to use
        deck_slug: Slug of the deck to use (optional)
        partner_slug: Partner slug for custom deck (optional)
        seed: Random seed for reproducible draws (optional)
        question: User's question (optional)
        
    Returns:
        Dictionary containing tarot reading data
        
    Raises:
        CalculationError: If drawing fails
    """
    try:
        # Set random seed if provided
        if seed is not None:
            random.seed(seed)
        
        # Load spread configuration
        spread = load_spread(spread_slug)
        
        # Load deck
        deck = load_deck(deck_slug, partner_slug)
        
        # Draw cards
        drawn_cards = draw_cards(deck, spread["card_count"])
        
        # Apply spread positions
        positioned_cards = apply_spread_positions(drawn_cards, spread)
        
        reading_data = {
            "spread": spread,
            "deck": {
                "slug": deck_slug or settings.DEFAULT_TAROT_DECK,
                "name": deck["name"],
                "description": deck.get("description"),
            },
            "question": question,
            "cards": positioned_cards,
            "metadata": {
                "seed": seed,
                "draw_time": None,  # Will be set by calling service
                "partner_slug": partner_slug,
            },
        }
        
        return reading_data
        
    except Exception as e:
        raise CalculationError("tarot", f"Failed to draw tarot reading: {str(e)}")


def load_spread(spread_slug: str) -> Dict[str, Any]:
    """Load spread configuration from JSON file."""
    try:
        # Try to load from data directory first
        spread_file = Path("data/spreads") / f"{spread_slug}.json"
        
        if not spread_file.exists():
            # Fall back to default spreads
            spread_file = Path("data/spreads/default.json")
            
        with open(spread_file, "r", encoding="utf-8") as f:
            spreads = json.load(f)
            
        # Find the specific spread
        for spread in spreads.get("spreads", []):
            if spread.get("slug") == spread_slug:
                return spread
                
        # If not found, return default spread
        return get_default_spread(spread_slug)
        
    except Exception as e:
        raise CalculationError("tarot", f"Failed to load spread '{spread_slug}': {str(e)}")


def load_deck(deck_slug: str = None, partner_slug: str = None) -> Dict[str, Any]:
    """Load deck configuration and cards."""
    try:
        deck_slug = deck_slug or settings.DEFAULT_TAROT_DECK
        
        # Try partner-specific deck first
        if partner_slug:
            partner_deck_file = Path(f"partners/{partner_slug}/deck/deck.json")
            if partner_deck_file.exists():
                with open(partner_deck_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        
        # Fall back to default deck
        deck_file = Path("data/decks") / f"{deck_slug}.json"
        
        if not deck_file.exists():
            deck_file = Path("data/decks/rider_waite_smith.json")
            
        with open(deck_file, "r", encoding="utf-8") as f:
            return json.load(f)
            
    except Exception as e:
        raise CalculationError("tarot", f"Failed to load deck '{deck_slug}': {str(e)}")


def draw_cards(deck: Dict[str, Any], count: int) -> List[Dict[str, Any]]:
    """Draw specified number of cards from deck."""
    cards = deck.get("cards", [])
    
    if len(cards) < count:
        raise CalculationError("tarot", f"Deck has only {len(cards)} cards, cannot draw {count}")
    
    # Shuffle and draw cards
    available_cards = cards.copy()
    random.shuffle(available_cards)
    drawn_cards = available_cards[:count]
    
    # Add orientation (upright/reversed) to each card
    for card in drawn_cards:
        card["reversed"] = random.random() < settings.REVERSAL_PROBABILITY
        
    return drawn_cards


def apply_spread_positions(cards: List[Dict[str, Any]], spread: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Apply spread positions to drawn cards."""
    positions = spread.get("positions", [])
    positioned_cards = []
    
    for i, card in enumerate(cards):
        if i < len(positions):
            position = positions[i]
            positioned_card = {
                **card,
                "position": {
                    "index": i,
                    "name": position.get("name"),
                    "description": position.get("description"),
                    "x": position.get("x", 0),
                    "y": position.get("y", 0),
                    "rotation": position.get("rotation", 0),
                }
            }
            positioned_cards.append(positioned_card)
    
    return positioned_cards


def get_default_spread(spread_slug: str) -> Dict[str, Any]:
    """Get default spread configuration."""
    default_spreads = {
        "one_card": {
            "slug": "one_card",
            "name": "One Card",
            "description": "A simple one-card draw for quick guidance",
            "card_count": 1,
            "positions": [
                {
                    "name": "Guidance",
                    "description": "What you need to know right now",
                    "x": 0,
                    "y": 0,
                    "rotation": 0
                }
            ]
        },
        "three_card": {
            "slug": "three_card",
            "name": "Three Card",
            "description": "Past, Present, Future spread",
            "card_count": 3,
            "positions": [
                {
                    "name": "Past",
                    "description": "Past influences affecting the situation",
                    "x": -1,
                    "y": 0,
                    "rotation": 0
                },
                {
                    "name": "Present",
                    "description": "Current situation and energies",
                    "x": 0,
                    "y": 0,
                    "rotation": 0
                },
                {
                    "name": "Future",
                    "description": "Likely outcome or future influences",
                    "x": 1,
                    "y": 0,
                    "rotation": 0
                }
            ]
        },
        "celtic_cross": {
            "slug": "celtic_cross",
            "name": "Celtic Cross",
            "description": "Comprehensive 10-card spread for deep insight",
            "card_count": 10,
            "positions": [
                {"name": "Present Situation", "description": "Current state of affairs", "x": 0, "y": 0, "rotation": 0},
                {"name": "Challenge", "description": "What crosses you or challenges you", "x": 0, "y": 0, "rotation": 90},
                {"name": "Distant Past", "description": "Foundation of the situation", "x": 0, "y": -1, "rotation": 0},
                {"name": "Recent Past", "description": "Recent events leading to now", "x": -1, "y": 0, "rotation": 0},
                {"name": "Possible Outcome", "description": "What may come to pass", "x": 0, "y": 1, "rotation": 0},
                {"name": "Near Future", "description": "What is approaching", "x": 1, "y": 0, "rotation": 0},
                {"name": "Your Approach", "description": "How you approach the situation", "x": 2, "y": 1, "rotation": 0},
                {"name": "External Influences", "description": "How others see you", "x": 2, "y": 0, "rotation": 0},
                {"name": "Hopes and Fears", "description": "Your inner feelings", "x": 2, "y": -1, "rotation": 0},
                {"name": "Final Outcome", "description": "The ultimate result", "x": 2, "y": -2, "rotation": 0}
            ]
        }
    }
    
    return default_spreads.get(spread_slug, default_spreads["three_card"])


def interpret_card(card: Dict[str, Any], position: Dict[str, Any] = None) -> Dict[str, Any]:
    """Interpret a single card in context."""
    interpretation = {
        "card_name": card.get("name"),
        "reversed": card.get("reversed", False),
        "position_name": position.get("name") if position else None,
        "meaning": get_card_meaning(card),
        "keywords": get_card_keywords(card),
        "advice": get_card_advice(card, position),
    }
    
    return interpretation


def get_card_meaning(card: Dict[str, Any]) -> str:
    """Get meaning for a card based on orientation."""
    if card.get("reversed"):
        return card.get("reversed_meaning", card.get("upright_meaning", ""))
    else:
        return card.get("upright_meaning", "")


def get_card_keywords(card: Dict[str, Any]) -> List[str]:
    """Get keywords for a card based on orientation."""
    if card.get("reversed"):
        return card.get("keywords_reversed", card.get("keywords_upright", []))
    else:
        return card.get("keywords_upright", [])


def get_card_advice(card: Dict[str, Any], position: Dict[str, Any] = None) -> str:
    """Generate advice based on card and position."""
    # This would be enhanced with more sophisticated interpretation logic
    meaning = get_card_meaning(card)
    position_name = position.get("name") if position else "general guidance"
    
    return f"In the position of {position_name}, {card.get('name')} suggests: {meaning}"


def calculate_reading_themes(cards: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate overall themes and patterns in the reading."""
    themes = {
        "major_arcana_count": 0,
        "minor_arcana_count": 0,
        "reversed_count": 0,
        "suits": {"cups": 0, "wands": 0, "swords": 0, "pentacles": 0},
        "elements": {"water": 0, "fire": 0, "air": 0, "earth": 0},
        "dominant_suit": None,
        "dominant_element": None,
        "overall_energy": "balanced",
    }
    
    for card in cards:
        # Count arcana types
        if card.get("arcana") == "major":
            themes["major_arcana_count"] += 1
        else:
            themes["minor_arcana_count"] += 1
            
        # Count reversed cards
        if card.get("reversed"):
            themes["reversed_count"] += 1
            
        # Count suits and elements
        suit = card.get("suit", "").lower()
        if suit in themes["suits"]:
            themes["suits"][suit] += 1
            
        element = get_suit_element(suit)
        if element in themes["elements"]:
            themes["elements"][element] += 1
    
    # Determine dominant suit and element
    themes["dominant_suit"] = max(themes["suits"], key=themes["suits"].get)
    themes["dominant_element"] = max(themes["elements"], key=themes["elements"].get)
    
    # Determine overall energy
    if themes["reversed_count"] > len(cards) / 2:
        themes["overall_energy"] = "challenging"
    elif themes["major_arcana_count"] > themes["minor_arcana_count"]:
        themes["overall_energy"] = "spiritual"
    else:
        themes["overall_energy"] = "practical"
    
    return themes


def get_suit_element(suit: str) -> str:
    """Get element for tarot suit."""
    suit_elements = {
        "cups": "water",
        "wands": "fire", 
        "swords": "air",
        "pentacles": "earth"
    }
    return suit_elements.get(suit, "")


def validate_deck(deck_data: Dict[str, Any]) -> bool:
    """Validate deck data structure."""
    required_fields = ["name", "cards"]
    
    if not all(field in deck_data for field in required_fields):
        return False
        
    cards = deck_data.get("cards", [])
    if not cards:
        return False
        
    # Validate each card has required fields
    required_card_fields = ["name", "arcana"]
    for card in cards:
        if not all(field in card for field in required_card_fields):
            return False
            
    return True


def validate_spread(spread_data: Dict[str, Any]) -> bool:
    """Validate spread data structure."""
    required_fields = ["name", "card_count", "positions"]
    
    if not all(field in spread_data for field in required_fields):
        return False
        
    positions = spread_data.get("positions", [])
    card_count = spread_data.get("card_count", 0)
    
    if len(positions) != card_count:
        return False
        
    # Validate each position has required fields
    required_position_fields = ["name", "description"]
    for position in positions:
        if not all(field in position for field in required_position_fields):
            return False
            
    return True
