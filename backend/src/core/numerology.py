"""
Numerology calculation module.

Provides core numerology calculations including life path, expression, 
soul urge, and personality numbers.
"""

from datetime import datetime
from typing import Dict, Any, Optional

from src.core.exceptions import CalculationError


def calculate_numerology_profile(
    birth_date: datetime,
    full_name: str,
    birth_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Calculate complete numerology profile.
    
    Args:
        birth_date: Date of birth
        full_name: Current full name
        birth_name: Birth name if different from current name
        
    Returns:
        Dictionary containing numerology data
        
    Raises:
        CalculationError: If calculation fails
    """
    try:
        profile = {
            "birth_info": {
                "date": birth_date.isoformat(),
                "full_name": full_name,
                "birth_name": birth_name,
            },
            "core_numbers": {
                "life_path": calculate_life_path_number(birth_date),
                "expression": calculate_expression_number(full_name),
                "soul_urge": calculate_soul_urge_number(full_name),
                "personality": calculate_personality_number(full_name),
                "birthday": calculate_birthday_number(birth_date),
            },
            "additional_numbers": {
                "maturity": None,  # Will be calculated
                "balance": None,   # Will be calculated
                "karmic_debt": calculate_karmic_debt_numbers(birth_date, full_name),
                "master_numbers": find_master_numbers(birth_date, full_name),
            },
            "cycles": {
                "personal_year": calculate_personal_year(birth_date),
                "personal_month": calculate_personal_month(birth_date),
                "personal_day": calculate_personal_day(birth_date),
            },
        }
        
        # Calculate derived numbers
        profile["additional_numbers"]["maturity"] = calculate_maturity_number(
            profile["core_numbers"]["life_path"],
            profile["core_numbers"]["expression"]
        )
        
        profile["additional_numbers"]["balance"] = calculate_balance_number(full_name)
        
        return profile
        
    except Exception as e:
        raise CalculationError("numerology", f"Failed to calculate numerology profile: {str(e)}")


def calculate_life_path_number(birth_date: datetime) -> Dict[str, Any]:
    """Calculate life path number from birth date."""
    # Convert date to string and sum digits
    date_str = f"{birth_date.month:02d}{birth_date.day:02d}{birth_date.year}"
    total = sum(int(digit) for digit in date_str)
    
    # Reduce to single digit (except master numbers)
    reduced = reduce_to_single_digit(total, keep_master=True)
    
    return {
        "number": reduced,
        "calculation": f"{date_str} = {total} = {reduced}",
        "meaning": get_life_path_meaning(reduced),
        "is_master": reduced in [11, 22, 33],
    }


def calculate_expression_number(full_name: str) -> Dict[str, Any]:
    """Calculate expression number from full name."""
    total = sum(get_letter_value(char) for char in full_name.upper() if char.isalpha())
    reduced = reduce_to_single_digit(total, keep_master=True)
    
    return {
        "number": reduced,
        "calculation": f"{full_name} = {total} = {reduced}",
        "meaning": get_expression_meaning(reduced),
        "is_master": reduced in [11, 22, 33],
    }


def calculate_soul_urge_number(full_name: str) -> Dict[str, Any]:
    """Calculate soul urge number from vowels in name."""
    vowels = "AEIOU"
    total = sum(get_letter_value(char) for char in full_name.upper() if char in vowels)
    reduced = reduce_to_single_digit(total, keep_master=True)
    
    return {
        "number": reduced,
        "calculation": f"Vowels in {full_name} = {total} = {reduced}",
        "meaning": get_soul_urge_meaning(reduced),
        "is_master": reduced in [11, 22, 33],
    }


def calculate_personality_number(full_name: str) -> Dict[str, Any]:
    """Calculate personality number from consonants in name."""
    vowels = "AEIOU"
    total = sum(get_letter_value(char) for char in full_name.upper() 
               if char.isalpha() and char not in vowels)
    reduced = reduce_to_single_digit(total, keep_master=True)
    
    return {
        "number": reduced,
        "calculation": f"Consonants in {full_name} = {total} = {reduced}",
        "meaning": get_personality_meaning(reduced),
        "is_master": reduced in [11, 22, 33],
    }


def calculate_birthday_number(birth_date: datetime) -> Dict[str, Any]:
    """Calculate birthday number from day of birth."""
    day = birth_date.day
    reduced = reduce_to_single_digit(day, keep_master=True)
    
    return {
        "number": reduced,
        "calculation": f"Day {day} = {reduced}",
        "meaning": get_birthday_meaning(reduced),
        "is_master": reduced in [11, 22, 33],
    }


def calculate_maturity_number(life_path: Dict[str, Any], expression: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate maturity number from life path and expression."""
    total = life_path["number"] + expression["number"]
    reduced = reduce_to_single_digit(total, keep_master=True)
    
    return {
        "number": reduced,
        "calculation": f"{life_path['number']} + {expression['number']} = {total} = {reduced}",
        "meaning": get_maturity_meaning(reduced),
        "is_master": reduced in [11, 22, 33],
    }


def calculate_balance_number(full_name: str) -> Dict[str, Any]:
    """Calculate balance number from first letter of each name."""
    names = full_name.split()
    total = sum(get_letter_value(name[0]) for name in names if name)
    reduced = reduce_to_single_digit(total, keep_master=True)
    
    return {
        "number": reduced,
        "calculation": f"First letters = {total} = {reduced}",
        "meaning": get_balance_meaning(reduced),
        "is_master": reduced in [11, 22, 33],
    }


def calculate_personal_year(birth_date: datetime) -> int:
    """Calculate personal year number."""
    current_year = datetime.now().year
    month_day = f"{birth_date.month:02d}{birth_date.day:02d}"
    total = sum(int(digit) for digit in f"{month_day}{current_year}")
    return reduce_to_single_digit(total)


def calculate_personal_month(birth_date: datetime) -> int:
    """Calculate personal month number."""
    personal_year = calculate_personal_year(birth_date)
    current_month = datetime.now().month
    total = personal_year + current_month
    return reduce_to_single_digit(total)


def calculate_personal_day(birth_date: datetime) -> int:
    """Calculate personal day number."""
    personal_month = calculate_personal_month(birth_date)
    current_day = datetime.now().day
    total = personal_month + current_day
    return reduce_to_single_digit(total)


def calculate_karmic_debt_numbers(birth_date: datetime, full_name: str) -> list:
    """Find karmic debt numbers (13, 14, 16, 19)."""
    karmic_debt = []
    
    # Check life path for karmic debt
    date_str = f"{birth_date.month:02d}{birth_date.day:02d}{birth_date.year}"
    total = sum(int(digit) for digit in date_str)
    if total in [13, 14, 16, 19]:
        karmic_debt.append(total)
    
    # Check expression for karmic debt
    name_total = sum(get_letter_value(char) for char in full_name.upper() if char.isalpha())
    if name_total in [13, 14, 16, 19]:
        karmic_debt.append(name_total)
    
    return list(set(karmic_debt))  # Remove duplicates


def find_master_numbers(birth_date: datetime, full_name: str) -> list:
    """Find master numbers (11, 22, 33) in the profile."""
    master_numbers = []
    
    # Check various calculations for master numbers
    calculations = [
        sum(int(digit) for digit in f"{birth_date.month:02d}{birth_date.day:02d}{birth_date.year}"),
        sum(get_letter_value(char) for char in full_name.upper() if char.isalpha()),
    ]
    
    for calc in calculations:
        # Check intermediate sums for master numbers
        while calc > 33:
            if calc in [11, 22, 33]:
                master_numbers.append(calc)
            calc = sum(int(digit) for digit in str(calc))
    
    return list(set(master_numbers))


def get_letter_value(letter: str) -> int:
    """Get numerological value for a letter."""
    values = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }
    return values.get(letter.upper(), 0)


def reduce_to_single_digit(number: int, keep_master: bool = False) -> int:
    """Reduce number to single digit, optionally keeping master numbers."""
    while number > 9:
        if keep_master and number in [11, 22, 33]:
            break
        number = sum(int(digit) for digit in str(number))
    return number


# Meaning functions (simplified for brevity)
def get_life_path_meaning(number: int) -> str:
    """Get meaning for life path number."""
    meanings = {
        1: "Leadership and independence",
        2: "Cooperation and harmony",
        3: "Creativity and communication",
        4: "Stability and hard work",
        5: "Freedom and adventure",
        6: "Nurturing and responsibility",
        7: "Spirituality and introspection",
        8: "Material success and power",
        9: "Humanitarian service",
        11: "Spiritual illumination",
        22: "Master builder",
        33: "Master teacher",
    }
    return meanings.get(number, "Unknown")


def get_expression_meaning(number: int) -> str:
    """Get meaning for expression number."""
    return get_life_path_meaning(number)  # Simplified


def get_soul_urge_meaning(number: int) -> str:
    """Get meaning for soul urge number."""
    return get_life_path_meaning(number)  # Simplified


def get_personality_meaning(number: int) -> str:
    """Get meaning for personality number."""
    return get_life_path_meaning(number)  # Simplified


def get_birthday_meaning(number: int) -> str:
    """Get meaning for birthday number."""
    return get_life_path_meaning(number)  # Simplified


def get_maturity_meaning(number: int) -> str:
    """Get meaning for maturity number."""
    return get_life_path_meaning(number)  # Simplified


def get_balance_meaning(number: int) -> str:
    """Get meaning for balance number."""
    return get_life_path_meaning(number)  # Simplified
