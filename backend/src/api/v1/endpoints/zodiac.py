"""
Chinese Zodiac endpoints for animal and element calculations.
"""

from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.core import zodiac
from src.core.exceptions import CalculationError

router = APIRouter()


class ZodiacRequest(BaseModel):
    """Request schema for Chinese zodiac calculation."""
    
    birth_date: datetime = Field(..., description="Date of birth")


@router.post("/calculate")
async def calculate_chinese_zodiac(request: ZodiacRequest):
    """
    Calculate Chinese zodiac animal and element.
    
    Returns the zodiac animal, element, polarity (yin/yang), compatibility,
    personality traits, and fortune information based on birth year.
    """
    try:
        zodiac_data = zodiac.calculate_chinese_zodiac(request.birth_date)
        
        return {
            "success": True,
            "data": zodiac_data
        }
        
    except CalculationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/animals")
async def get_zodiac_animals():
    """
    Get information about all Chinese zodiac animals.
    
    Returns details about each animal including traits, compatibility,
    lucky numbers, colors, and directions.
    """
    animals = [
        {
            "name": "Rat",
            "chinese_name": "鼠",
            "order": 1,
            "years": [1924, 1936, 1948, 1960, 1972, 1984, 1996, 2008, 2020, 2032],
            "traits": {
                "positive": ["Intelligent", "Adaptable", "Charming", "Resourceful"],
                "negative": ["Opportunistic", "Restless", "Scheming"],
                "personality": "Quick-witted and versatile"
            },
            "compatibility": {
                "best": ["Dragon", "Monkey"],
                "good": ["Ox"],
                "avoid": ["Horse"]
            },
            "fortune": {
                "lucky_numbers": [2, 3],
                "lucky_colors": ["Blue", "Gold", "Green"],
                "lucky_directions": ["Southeast", "Northeast"],
                "unlucky_numbers": [5, 9],
                "unlucky_colors": ["Yellow", "Brown"]
            }
        },
        {
            "name": "Ox",
            "chinese_name": "牛",
            "order": 2,
            "years": [1925, 1937, 1949, 1961, 1973, 1985, 1997, 2009, 2021, 2033],
            "traits": {
                "positive": ["Reliable", "Patient", "Methodical", "Honest"],
                "negative": ["Stubborn", "Conservative", "Slow"],
                "personality": "Dependable and hardworking"
            },
            "compatibility": {
                "best": ["Snake", "Rooster"],
                "good": ["Rat"],
                "avoid": ["Goat"]
            },
            "fortune": {
                "lucky_numbers": [1, 9],
                "lucky_colors": ["White", "Yellow", "Green"],
                "lucky_directions": ["North", "South"],
                "unlucky_numbers": [3, 4],
                "unlucky_colors": ["Blue", "Green"]
            }
        },
        {
            "name": "Tiger",
            "chinese_name": "虎",
            "order": 3,
            "years": [1926, 1938, 1950, 1962, 1974, 1986, 1998, 2010, 2022, 2034],
            "traits": {
                "positive": ["Brave", "Confident", "Charismatic", "Generous"],
                "negative": ["Impulsive", "Rebellious", "Unpredictable"],
                "personality": "Bold and adventurous"
            },
            "compatibility": {
                "best": ["Horse", "Dog"],
                "good": ["Pig"],
                "avoid": ["Monkey"]
            },
            "fortune": {
                "lucky_numbers": [1, 3, 4],
                "lucky_colors": ["Blue", "Gray", "Orange"],
                "lucky_directions": ["South", "East"],
                "unlucky_numbers": [6, 7, 8],
                "unlucky_colors": ["Brown", "Yellow"]
            }
        },
        {
            "name": "Rabbit",
            "chinese_name": "兔",
            "order": 4,
            "years": [1927, 1939, 1951, 1963, 1975, 1987, 1999, 2011, 2023, 2035],
            "traits": {
                "positive": ["Gentle", "Elegant", "Compassionate", "Lucky"],
                "negative": ["Timid", "Pessimistic", "Superficial"],
                "personality": "Peaceful and refined"
            },
            "compatibility": {
                "best": ["Goat", "Pig"],
                "good": ["Dog"],
                "avoid": ["Rooster"]
            },
            "fortune": {
                "lucky_numbers": [3, 4, 6],
                "lucky_colors": ["Red", "Pink", "Purple"],
                "lucky_directions": ["East", "Southeast"],
                "unlucky_numbers": [1, 7, 8],
                "unlucky_colors": ["Dark Brown", "Dark Yellow"]
            }
        },
        {
            "name": "Dragon",
            "chinese_name": "龙",
            "order": 5,
            "years": [1928, 1940, 1952, 1964, 1976, 1988, 2000, 2012, 2024, 2036],
            "traits": {
                "positive": ["Energetic", "Intelligent", "Ambitious", "Lucky"],
                "negative": ["Arrogant", "Impatient", "Demanding"],
                "personality": "Powerful and charismatic"
            },
            "compatibility": {
                "best": ["Rat", "Monkey"],
                "good": ["Rooster"],
                "avoid": ["Dog"]
            },
            "fortune": {
                "lucky_numbers": [1, 6, 7],
                "lucky_colors": ["Gold", "Silver", "Gray"],
                "lucky_directions": ["North", "West"],
                "unlucky_numbers": [3, 8, 9],
                "unlucky_colors": ["Blue", "Green"]
            }
        },
        {
            "name": "Snake",
            "chinese_name": "蛇",
            "order": 6,
            "years": [1929, 1941, 1953, 1965, 1977, 1989, 2001, 2013, 2025, 2037],
            "traits": {
                "positive": ["Wise", "Intuitive", "Graceful", "Mysterious"],
                "negative": ["Jealous", "Suspicious", "Cunning"],
                "personality": "Enigmatic and philosophical"
            },
            "compatibility": {
                "best": ["Ox", "Rooster"],
                "good": ["Dragon"],
                "avoid": ["Pig"]
            },
            "fortune": {
                "lucky_numbers": [2, 8, 9],
                "lucky_colors": ["Black", "Red", "Yellow"],
                "lucky_directions": ["Southwest", "West"],
                "unlucky_numbers": [1, 6, 7],
                "unlucky_colors": ["Brown", "White"]
            }
        }
    ]
    
    return {
        "success": True,
        "data": {
            "animals": animals,
            "total_animals": 12,
            "cycle_years": 12
        }
    }


@router.get("/elements")
async def get_zodiac_elements():
    """
    Get information about Chinese zodiac elements.
    
    Returns details about the five elements (Wood, Fire, Earth, Metal, Water)
    and their characteristics, cycles, and influences.
    """
    elements = [
        {
            "name": "Wood",
            "chinese_name": "木",
            "years": [1924, 1925, 1934, 1935, 1944, 1945, 1954, 1955, 1964, 1965],
            "characteristics": {
                "nature": "Growth and expansion",
                "personality": "Creative, idealistic, and cooperative",
                "direction": "East",
                "season": "Spring",
                "color": "Green",
                "traits": ["Creative", "Flexible", "Intuitive", "Generous"]
            }
        },
        {
            "name": "Fire",
            "chinese_name": "火",
            "years": [1926, 1927, 1936, 1937, 1946, 1947, 1956, 1957, 1966, 1967],
            "characteristics": {
                "nature": "Energy and passion",
                "personality": "Dynamic, enthusiastic, and leadership-oriented",
                "direction": "South",
                "season": "Summer",
                "color": "Red",
                "traits": ["Energetic", "Passionate", "Charismatic", "Adventurous"]
            }
        },
        {
            "name": "Earth",
            "chinese_name": "土",
            "years": [1928, 1929, 1938, 1939, 1948, 1949, 1958, 1959, 1968, 1969],
            "characteristics": {
                "nature": "Stability and grounding",
                "personality": "Practical, reliable, and nurturing",
                "direction": "Center",
                "season": "Late Summer",
                "color": "Yellow",
                "traits": ["Stable", "Practical", "Reliable", "Nurturing"]
            }
        },
        {
            "name": "Metal",
            "chinese_name": "金",
            "years": [1930, 1931, 1940, 1941, 1950, 1951, 1960, 1961, 1970, 1971],
            "characteristics": {
                "nature": "Structure and discipline",
                "personality": "Organized, determined, and ambitious",
                "direction": "West",
                "season": "Autumn",
                "color": "White",
                "traits": ["Organized", "Determined", "Strong-willed", "Ambitious"]
            }
        },
        {
            "name": "Water",
            "chinese_name": "水",
            "years": [1932, 1933, 1942, 1943, 1952, 1953, 1962, 1963, 1972, 1973],
            "characteristics": {
                "nature": "Flow and adaptability",
                "personality": "Intuitive, flexible, and diplomatic",
                "direction": "North",
                "season": "Winter",
                "color": "Black/Blue",
                "traits": ["Intuitive", "Flexible", "Diplomatic", "Wise"]
            }
        }
    ]
    
    return {
        "success": True,
        "data": {
            "elements": elements,
            "cycle": {
                "productive": "Wood feeds Fire, Fire creates Earth, Earth bears Metal, Metal collects Water, Water nourishes Wood",
                "destructive": "Wood depletes Earth, Earth absorbs Water, Water extinguishes Fire, Fire melts Metal, Metal cuts Wood"
            },
            "total_elements": 5,
            "cycle_years": 10
        }
    }


@router.get("/compatibility/{animal1}/{animal2}")
async def get_compatibility(animal1: str, animal2: str):
    """
    Get compatibility between two Chinese zodiac animals.
    
    Returns detailed compatibility analysis including overall score,
    strengths, challenges, and advice for the relationship.
    """
    try:
        # Get compatibility data for both animals
        compatibility1 = zodiac.get_animal_compatibility(animal1.title())
        compatibility2 = zodiac.get_animal_compatibility(animal2.title())
        
        # Determine compatibility level
        if animal2.title() in compatibility1.get("best", []):
            level = "excellent"
            score = 90
            description = "Excellent compatibility with natural harmony and understanding"
        elif animal2.title() in compatibility1.get("good", []):
            level = "good"
            score = 75
            description = "Good compatibility with potential for strong relationship"
        elif animal2.title() in compatibility1.get("avoid", []):
            level = "challenging"
            score = 40
            description = "Challenging compatibility requiring extra effort and understanding"
        else:
            level = "neutral"
            score = 60
            description = "Neutral compatibility with balanced potential"
        
        return {
            "success": True,
            "data": {
                "animal1": animal1.title(),
                "animal2": animal2.title(),
                "compatibility": {
                    "level": level,
                    "score": score,
                    "description": description
                },
                "animal1_compatibility": compatibility1,
                "animal2_compatibility": compatibility2
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
