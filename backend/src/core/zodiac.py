"""
Chinese Zodiac calculation module.

Provides Chinese zodiac animal and element calculations based on birth year.
"""

from datetime import datetime
from typing import Dict, Any

from src.core.exceptions import CalculationError


def calculate_chinese_zodiac(birth_date: datetime) -> Dict[str, Any]:
    """
    Calculate Chinese zodiac animal and element.
    
    Args:
        birth_date: Date of birth
        
    Returns:
        Dictionary containing Chinese zodiac data
        
    Raises:
        CalculationError: If calculation fails
    """
    try:
        year = birth_date.year
        
        # Calculate animal
        animal = get_zodiac_animal(year)
        
        # Calculate element
        element = get_zodiac_element(year)
        
        # Calculate yin/yang
        polarity = get_zodiac_polarity(year)
        
        # Get compatibility info
        compatibility = get_animal_compatibility(animal)
        
        # Get personality traits
        traits = get_animal_traits(animal)
        
        zodiac_data = {
            "birth_info": {
                "year": year,
                "date": birth_date.isoformat(),
            },
            "animal": {
                "name": animal,
                "chinese_name": get_chinese_name(animal),
                "order": get_animal_order(animal),
                "traits": traits,
            },
            "element": {
                "name": element,
                "chinese_name": get_element_chinese_name(element),
                "characteristics": get_element_characteristics(element),
            },
            "polarity": {
                "type": polarity,
                "meaning": get_polarity_meaning(polarity),
            },
            "compatibility": compatibility,
            "fortune": {
                "lucky_numbers": get_lucky_numbers(animal),
                "lucky_colors": get_lucky_colors(animal),
                "lucky_directions": get_lucky_directions(animal),
                "unlucky_numbers": get_unlucky_numbers(animal),
                "unlucky_colors": get_unlucky_colors(animal),
            },
        }
        
        return zodiac_data
        
    except Exception as e:
        raise CalculationError("chinese_zodiac", f"Failed to calculate Chinese zodiac: {str(e)}")


def get_zodiac_animal(year: int) -> str:
    """Get zodiac animal for given year."""
    animals = [
        "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
        "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"
    ]
    
    # Chinese zodiac starts from 1924 (Rat year) in this calculation
    # Adjust for the actual Chinese New Year if needed
    base_year = 1924
    index = (year - base_year) % 12
    return animals[index]


def get_zodiac_element(year: int) -> str:
    """Get zodiac element for given year."""
    elements = ["Wood", "Fire", "Earth", "Metal", "Water"]
    
    # Each element lasts 2 years, cycle repeats every 10 years
    base_year = 1924
    cycle_position = (year - base_year) % 10
    index = cycle_position // 2
    return elements[index]


def get_zodiac_polarity(year: int) -> str:
    """Get yin/yang polarity for given year."""
    # Even years are Yang, odd years are Yin
    return "Yang" if year % 2 == 0 else "Yin"


def get_chinese_name(animal: str) -> str:
    """Get Chinese name for zodiac animal."""
    chinese_names = {
        "Rat": "鼠", "Ox": "牛", "Tiger": "虎", "Rabbit": "兔",
        "Dragon": "龙", "Snake": "蛇", "Horse": "马", "Goat": "羊",
        "Monkey": "猴", "Rooster": "鸡", "Dog": "狗", "Pig": "猪"
    }
    return chinese_names.get(animal, "")


def get_element_chinese_name(element: str) -> str:
    """Get Chinese name for element."""
    chinese_names = {
        "Wood": "木", "Fire": "火", "Earth": "土", "Metal": "金", "Water": "水"
    }
    return chinese_names.get(element, "")


def get_animal_order(animal: str) -> int:
    """Get order position of animal in zodiac cycle."""
    animals = [
        "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
        "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"
    ]
    return animals.index(animal) + 1 if animal in animals else 0


def get_animal_traits(animal: str) -> Dict[str, Any]:
    """Get personality traits for zodiac animal."""
    traits = {
        "Rat": {
            "positive": ["Intelligent", "Adaptable", "Charming", "Resourceful"],
            "negative": ["Opportunistic", "Restless", "Scheming"],
            "personality": "Quick-witted and versatile"
        },
        "Ox": {
            "positive": ["Reliable", "Patient", "Methodical", "Honest"],
            "negative": ["Stubborn", "Conservative", "Slow"],
            "personality": "Dependable and hardworking"
        },
        "Tiger": {
            "positive": ["Brave", "Confident", "Charismatic", "Generous"],
            "negative": ["Impulsive", "Rebellious", "Unpredictable"],
            "personality": "Bold and adventurous"
        },
        "Rabbit": {
            "positive": ["Gentle", "Elegant", "Compassionate", "Lucky"],
            "negative": ["Timid", "Pessimistic", "Superficial"],
            "personality": "Peaceful and refined"
        },
        "Dragon": {
            "positive": ["Energetic", "Intelligent", "Ambitious", "Lucky"],
            "negative": ["Arrogant", "Impatient", "Demanding"],
            "personality": "Powerful and charismatic"
        },
        "Snake": {
            "positive": ["Wise", "Intuitive", "Graceful", "Mysterious"],
            "negative": ["Jealous", "Suspicious", "Cunning"],
            "personality": "Enigmatic and philosophical"
        },
        "Horse": {
            "positive": ["Energetic", "Independent", "Cheerful", "Popular"],
            "negative": ["Impatient", "Selfish", "Reckless"],
            "personality": "Free-spirited and enthusiastic"
        },
        "Goat": {
            "positive": ["Creative", "Gentle", "Compassionate", "Generous"],
            "negative": ["Pessimistic", "Disorganized", "Vulnerable"],
            "personality": "Artistic and sensitive"
        },
        "Monkey": {
            "positive": ["Clever", "Curious", "Innovative", "Flexible"],
            "negative": ["Mischievous", "Restless", "Opportunistic"],
            "personality": "Witty and inventive"
        },
        "Rooster": {
            "positive": ["Honest", "Energetic", "Intelligent", "Confident"],
            "negative": ["Critical", "Impatient", "Eccentric"],
            "personality": "Proud and observant"
        },
        "Dog": {
            "positive": ["Loyal", "Honest", "Responsible", "Reliable"],
            "negative": ["Anxious", "Pessimistic", "Critical"],
            "personality": "Faithful and protective"
        },
        "Pig": {
            "positive": ["Honest", "Generous", "Reliable", "Optimistic"],
            "negative": ["Naive", "Gullible", "Lazy"],
            "personality": "Kind-hearted and sincere"
        }
    }
    return traits.get(animal, {"positive": [], "negative": [], "personality": ""})


def get_element_characteristics(element: str) -> Dict[str, str]:
    """Get characteristics for zodiac element."""
    characteristics = {
        "Wood": {
            "nature": "Growth and expansion",
            "personality": "Creative, idealistic, and cooperative",
            "direction": "East",
            "season": "Spring"
        },
        "Fire": {
            "nature": "Energy and passion",
            "personality": "Dynamic, enthusiastic, and leadership-oriented",
            "direction": "South",
            "season": "Summer"
        },
        "Earth": {
            "nature": "Stability and grounding",
            "personality": "Practical, reliable, and nurturing",
            "direction": "Center",
            "season": "Late Summer"
        },
        "Metal": {
            "nature": "Structure and discipline",
            "personality": "Organized, determined, and ambitious",
            "direction": "West",
            "season": "Autumn"
        },
        "Water": {
            "nature": "Flow and adaptability",
            "personality": "Intuitive, flexible, and diplomatic",
            "direction": "North",
            "season": "Winter"
        }
    }
    return characteristics.get(element, {})


def get_polarity_meaning(polarity: str) -> str:
    """Get meaning for yin/yang polarity."""
    meanings = {
        "Yin": "Passive, receptive, intuitive, feminine energy",
        "Yang": "Active, assertive, logical, masculine energy"
    }
    return meanings.get(polarity, "")


def get_animal_compatibility(animal: str) -> Dict[str, Any]:
    """Get compatibility information for zodiac animal."""
    compatibility = {
        "Rat": {"best": ["Dragon", "Monkey"], "good": ["Ox"], "avoid": ["Horse"]},
        "Ox": {"best": ["Snake", "Rooster"], "good": ["Rat"], "avoid": ["Goat"]},
        "Tiger": {"best": ["Horse", "Dog"], "good": ["Pig"], "avoid": ["Monkey"]},
        "Rabbit": {"best": ["Goat", "Pig"], "good": ["Dog"], "avoid": ["Rooster"]},
        "Dragon": {"best": ["Rat", "Monkey"], "good": ["Rooster"], "avoid": ["Dog"]},
        "Snake": {"best": ["Ox", "Rooster"], "good": ["Dragon"], "avoid": ["Pig"]},
        "Horse": {"best": ["Tiger", "Dog"], "good": ["Goat"], "avoid": ["Rat"]},
        "Goat": {"best": ["Rabbit", "Pig"], "good": ["Horse"], "avoid": ["Ox"]},
        "Monkey": {"best": ["Rat", "Dragon"], "good": ["Snake"], "avoid": ["Tiger"]},
        "Rooster": {"best": ["Ox", "Snake"], "good": ["Dragon"], "avoid": ["Rabbit"]},
        "Dog": {"best": ["Tiger", "Horse"], "good": ["Rabbit"], "avoid": ["Dragon"]},
        "Pig": {"best": ["Rabbit", "Goat"], "good": ["Tiger"], "avoid": ["Snake"]}
    }
    return compatibility.get(animal, {"best": [], "good": [], "avoid": []})


def get_lucky_numbers(animal: str) -> list:
    """Get lucky numbers for zodiac animal."""
    lucky_numbers = {
        "Rat": [2, 3], "Ox": [1, 9], "Tiger": [1, 3, 4],
        "Rabbit": [3, 4, 6], "Dragon": [1, 6, 7], "Snake": [2, 8, 9],
        "Horse": [2, 3, 7], "Goat": [3, 4, 9], "Monkey": [1, 7, 8],
        "Rooster": [5, 7, 8], "Dog": [3, 4, 9], "Pig": [2, 5, 8]
    }
    return lucky_numbers.get(animal, [])


def get_lucky_colors(animal: str) -> list:
    """Get lucky colors for zodiac animal."""
    lucky_colors = {
        "Rat": ["Blue", "Gold", "Green"], "Ox": ["White", "Yellow", "Green"],
        "Tiger": ["Blue", "Gray", "Orange"], "Rabbit": ["Red", "Pink", "Purple"],
        "Dragon": ["Gold", "Silver", "Gray"], "Snake": ["Black", "Red", "Yellow"],
        "Horse": ["Yellow", "Green"], "Goat": ["Brown", "Red", "Purple"],
        "Monkey": ["White", "Blue", "Gold"], "Rooster": ["Gold", "Brown", "Yellow"],
        "Dog": ["Red", "Green", "Purple"], "Pig": ["Yellow", "Gray", "Brown"]
    }
    return lucky_colors.get(animal, [])


def get_lucky_directions(animal: str) -> list:
    """Get lucky directions for zodiac animal."""
    lucky_directions = {
        "Rat": ["Southeast", "Northeast"], "Ox": ["North", "South"],
        "Tiger": ["South", "East"], "Rabbit": ["East", "Southeast"],
        "Dragon": ["North", "West"], "Snake": ["Southwest", "West"],
        "Horse": ["Northeast", "Southwest"], "Goat": ["North", "Northwest"],
        "Monkey": ["North", "Northwest"], "Rooster": ["South", "Southeast"],
        "Dog": ["South", "East"], "Pig": ["Southwest", "Northeast"]
    }
    return lucky_directions.get(animal, [])


def get_unlucky_numbers(animal: str) -> list:
    """Get unlucky numbers for zodiac animal."""
    unlucky_numbers = {
        "Rat": [5, 9], "Ox": [3, 4], "Tiger": [6, 7, 8],
        "Rabbit": [1, 7, 8], "Dragon": [3, 8, 9], "Snake": [1, 6, 7],
        "Horse": [1, 5, 6], "Goat": [6, 7, 8], "Monkey": [2, 5, 9],
        "Rooster": [1, 3, 9], "Dog": [1, 6, 7], "Pig": [1, 3, 7]
    }
    return unlucky_numbers.get(animal, [])


def get_unlucky_colors(animal: str) -> list:
    """Get unlucky colors for zodiac animal."""
    unlucky_colors = {
        "Rat": ["Yellow", "Brown"], "Ox": ["Blue", "Green"],
        "Tiger": ["Brown", "Yellow"], "Rabbit": ["Dark Brown", "Dark Yellow"],
        "Dragon": ["Blue", "Green"], "Snake": ["Brown", "White"],
        "Horse": ["Blue", "White"], "Goat": ["Dark Green"],
        "Monkey": ["Red", "Black"], "Rooster": ["Red", "Green"],
        "Dog": ["Blue", "White"], "Pig": ["Red", "Blue"]
    }
    return unlucky_colors.get(animal, [])
