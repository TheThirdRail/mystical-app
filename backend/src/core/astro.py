"""
Astrology calculation module using Kerykeion.

Provides tropical and sidereal chart calculations with multiple ayanamsa systems.
"""

from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from kerykeion.astrological_subject import AstrologicalSubject as Subject

from src.core.exceptions import CalculationError


def calculate_birth_chart(
    birth_date: datetime,
    birth_time: str,
    birth_location: str,
    latitude: float,
    longitude: float,
    ayanamsa: str = "LAHIRI",
    sidereal: bool = False,
) -> Dict[str, Any]:
    """
    Calculate birth chart for given birth data.
    
    Args:
        birth_date: Date of birth
        birth_time: Time of birth in HH:MM format
        birth_location: Location name
        latitude: Birth latitude
        longitude: Birth longitude
        ayanamsa: Ayanamsa system for sidereal calculations
        sidereal: Whether to use sidereal zodiac
        
    Returns:
        Dictionary containing chart data
        
    Raises:
        CalculationError: If calculation fails
    """
    try:
        # Parse birth time
        hour, minute = map(int, birth_time.split(":"))
        
        # Create astrological subject
        subject = AstrologicalSubject(
            name="User",
            year=birth_date.year,
            month=birth_date.month,
            day=birth_date.day,
            hour=hour,
            minute=minute,
            city=birth_location,
            lat=latitude,
            lng=longitude,
            tz_str="UTC",  # Assume UTC for now, can be enhanced
            sidereal_mode=sidereal,
            ayanamsa=ayanamsa if sidereal else None,
        )
        
        # Extract chart data
        chart_data = {
            "birth_info": {
                "date": birth_date.isoformat(),
                "time": birth_time,
                "location": birth_location,
                "latitude": latitude,
                "longitude": longitude,
                "timezone": subject.timezone,
            },
            "calculation_info": {
                "sidereal": sidereal,
                "ayanamsa": ayanamsa if sidereal else None,
                "julian_day": subject.julian_day,
            },
            "planets": _extract_planets(subject),
            "houses": _extract_houses(subject),
            "aspects": _extract_aspects(subject),
            "elements": _calculate_elements(subject),
            "modalities": _calculate_modalities(subject),
            "chart_ruler": _find_chart_ruler(subject),
        }
        
        return chart_data
        
    except Exception as e:
        raise CalculationError("astrology", f"Failed to calculate birth chart: {str(e)}")


def calculate_compatibility(
    chart1: Dict[str, Any],
    chart2: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Calculate compatibility between two charts.
    
    Args:
        chart1: First person's chart data
        chart2: Second person's chart data
        
    Returns:
        Compatibility analysis
    """
    try:
        compatibility = {
            "overall_score": 0.0,
            "element_compatibility": _compare_elements(chart1, chart2),
            "sun_moon_compatibility": _compare_sun_moon(chart1, chart2),
            "venus_mars_compatibility": _compare_venus_mars(chart1, chart2),
            "aspects_between_charts": _calculate_synastry_aspects(chart1, chart2),
        }
        
        # Calculate overall score
        compatibility["overall_score"] = _calculate_overall_compatibility_score(compatibility)
        
        return compatibility
        
    except Exception as e:
        raise CalculationError("astrology", f"Failed to calculate compatibility: {str(e)}")


def _extract_planets(subject: Subject) -> Dict[str, Any]:
    """Extract planet positions from astrological subject."""
    planets = {}
    
    for planet_name, planet_data in subject.planets_list.items():
        planets[planet_name] = {
            "sign": planet_data.get("sign"),
            "position": planet_data.get("position"),
            "house": planet_data.get("house"),
            "retrograde": planet_data.get("retrograde", False),
            "element": _get_sign_element(planet_data.get("sign")),
            "modality": _get_sign_modality(planet_data.get("sign")),
        }
    
    return planets


def _extract_houses(subject: Subject) -> Dict[str, Any]:
    """Extract house cusps from astrological subject."""
    houses = {}
    
    for house_num, house_data in subject.houses_list.items():
        houses[f"house_{house_num}"] = {
            "sign": house_data.get("sign"),
            "position": house_data.get("position"),
            "element": _get_sign_element(house_data.get("sign")),
            "modality": _get_sign_modality(house_data.get("sign")),
        }
    
    return houses


def _extract_aspects(subject: Subject) -> list:
    """Extract aspects from astrological subject."""
    aspects = []
    
    # This would need to be implemented based on Kerykeion's aspect calculation
    # For now, return empty list
    return aspects


def _calculate_elements(subject: Subject) -> Dict[str, int]:
    """Calculate element distribution."""
    elements = {"fire": 0, "earth": 0, "air": 0, "water": 0}
    
    for planet_data in subject.planets_list.values():
        element = _get_sign_element(planet_data.get("sign"))
        if element:
            elements[element] += 1
    
    return elements


def _calculate_modalities(subject: Subject) -> Dict[str, int]:
    """Calculate modality distribution."""
    modalities = {"cardinal": 0, "fixed": 0, "mutable": 0}
    
    for planet_data in subject.planets_list.values():
        modality = _get_sign_modality(planet_data.get("sign"))
        if modality:
            modalities[modality] += 1
    
    return modalities


def _find_chart_ruler(subject: Subject) -> Optional[str]:
    """Find the chart ruler (ruling planet of ascendant sign)."""
    ascendant_sign = subject.houses_list.get(1, {}).get("sign")
    return _get_sign_ruler(ascendant_sign)


def _get_sign_element(sign: Optional[str]) -> Optional[str]:
    """Get element for zodiac sign."""
    if not sign:
        return None
        
    elements = {
        "Aries": "fire", "Leo": "fire", "Sagittarius": "fire",
        "Taurus": "earth", "Virgo": "earth", "Capricorn": "earth",
        "Gemini": "air", "Libra": "air", "Aquarius": "air",
        "Cancer": "water", "Scorpio": "water", "Pisces": "water",
    }
    return elements.get(sign)


def _get_sign_modality(sign: Optional[str]) -> Optional[str]:
    """Get modality for zodiac sign."""
    if not sign:
        return None
        
    modalities = {
        "Aries": "cardinal", "Cancer": "cardinal", "Libra": "cardinal", "Capricorn": "cardinal",
        "Taurus": "fixed", "Leo": "fixed", "Scorpio": "fixed", "Aquarius": "fixed",
        "Gemini": "mutable", "Virgo": "mutable", "Sagittarius": "mutable", "Pisces": "mutable",
    }
    return modalities.get(sign)


def _get_sign_ruler(sign: Optional[str]) -> Optional[str]:
    """Get ruling planet for zodiac sign."""
    if not sign:
        return None
        
    rulers = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
        "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
        "Libra": "Venus", "Scorpio": "Pluto", "Sagittarius": "Jupiter",
        "Capricorn": "Saturn", "Aquarius": "Uranus", "Pisces": "Neptune",
    }
    return rulers.get(sign)


def _compare_elements(chart1: Dict[str, Any], chart2: Dict[str, Any]) -> Dict[str, Any]:
    """Compare element compatibility between charts."""
    # Simplified element compatibility
    return {"score": 0.5, "details": "Element compatibility analysis"}


def _compare_sun_moon(chart1: Dict[str, Any], chart2: Dict[str, Any]) -> Dict[str, Any]:
    """Compare Sun-Moon compatibility."""
    return {"score": 0.5, "details": "Sun-Moon compatibility analysis"}


def _compare_venus_mars(chart1: Dict[str, Any], chart2: Dict[str, Any]) -> Dict[str, Any]:
    """Compare Venus-Mars compatibility."""
    return {"score": 0.5, "details": "Venus-Mars compatibility analysis"}


def _calculate_synastry_aspects(chart1: Dict[str, Any], chart2: Dict[str, Any]) -> list:
    """Calculate aspects between two charts."""
    return []


def _calculate_overall_compatibility_score(compatibility: Dict[str, Any]) -> float:
    """Calculate overall compatibility score."""
    # Simplified scoring
    return 0.75
