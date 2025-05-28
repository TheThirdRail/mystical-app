"""
Base LLM provider interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response from LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Dictionary containing response and metadata
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get provider name."""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Get model name."""
        pass
    
    def validate_config(self) -> bool:
        """Validate provider configuration."""
        return self.api_key is not None
    
    def format_reading_prompt(
        self,
        astro_data: Dict[str, Any],
        numerology_data: Dict[str, Any],
        zodiac_data: Dict[str, Any],
        tarot_data: Dict[str, Any],
        question: Optional[str] = None,
        partner_prompt_stub: Optional[str] = None,
        persona_config: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Format a comprehensive reading prompt.
        
        Args:
            astro_data: Astrology calculation results
            numerology_data: Numerology calculation results
            zodiac_data: Chinese zodiac calculation results
            tarot_data: Tarot reading results
            question: User's question (optional)
            partner_prompt_stub: Partner-specific prompt addition
            persona_config: Persona configuration for voice customization
            
        Returns:
            Formatted prompt string
        """
        prompt_parts = []
        
        # Add partner prompt stub if provided
        if partner_prompt_stub:
            prompt_parts.append(partner_prompt_stub)
        
        # Add persona voice configuration
        if persona_config:
            voice_style = persona_config.get("voice_style")
            tone = persona_config.get("tone")
            if voice_style:
                prompt_parts.append(f"Speak in a {voice_style} voice.")
            if tone:
                prompt_parts.append(f"Use a {tone} tone throughout.")
        
        # Add user question if provided
        if question:
            prompt_parts.append(f"The user asks: '{question}'")
        
        # Add calculation results
        prompt_parts.extend([
            "Based on the following spiritual calculations, provide a comprehensive reading:",
            "",
            "ASTROLOGY:",
            self._format_astro_section(astro_data),
            "",
            "NUMEROLOGY:",
            self._format_numerology_section(numerology_data),
            "",
            "CHINESE ZODIAC:",
            self._format_zodiac_section(zodiac_data),
            "",
            "TAROT:",
            self._format_tarot_section(tarot_data),
            "",
            "Please weave these insights together into a cohesive, positive, and empowering reading.",
            "Focus on growth opportunities and frame any challenges as chances for improvement.",
            "Keep the reading between 800-1200 words."
        ])
        
        return "\n".join(prompt_parts)
    
    def _format_astro_section(self, astro_data: Dict[str, Any]) -> str:
        """Format astrology data for prompt."""
        if not astro_data:
            return "No astrology data available."
            
        lines = []
        
        # Birth info
        birth_info = astro_data.get("birth_info", {})
        lines.append(f"Birth Date: {birth_info.get('date', 'Unknown')}")
        lines.append(f"Location: {birth_info.get('location', 'Unknown')}")
        
        # Key planets
        planets = astro_data.get("planets", {})
        if planets:
            lines.append("Key Planetary Positions:")
            for planet, data in planets.items():
                if planet in ["Sun", "Moon", "Mercury", "Venus", "Mars"]:
                    sign = data.get("sign", "Unknown")
                    house = data.get("house", "Unknown")
                    lines.append(f"  {planet}: {sign} in House {house}")
        
        # Elements and modalities
        elements = astro_data.get("elements", {})
        if elements:
            dominant_element = max(elements, key=elements.get)
            lines.append(f"Dominant Element: {dominant_element}")
        
        return "\n".join(lines)
    
    def _format_numerology_section(self, numerology_data: Dict[str, Any]) -> str:
        """Format numerology data for prompt."""
        if not numerology_data:
            return "No numerology data available."
            
        lines = []
        core_numbers = numerology_data.get("core_numbers", {})
        
        for number_type, data in core_numbers.items():
            if isinstance(data, dict):
                number = data.get("number")
                meaning = data.get("meaning", "")
                lines.append(f"{number_type.replace('_', ' ').title()}: {number} - {meaning}")
        
        return "\n".join(lines)
    
    def _format_zodiac_section(self, zodiac_data: Dict[str, Any]) -> str:
        """Format Chinese zodiac data for prompt."""
        if not zodiac_data:
            return "No Chinese zodiac data available."
            
        lines = []
        
        animal = zodiac_data.get("animal", {})
        element = zodiac_data.get("element", {})
        polarity = zodiac_data.get("polarity", {})
        
        if animal:
            lines.append(f"Animal: {animal.get('name')} - {animal.get('traits', {}).get('personality', '')}")
        
        if element:
            lines.append(f"Element: {element.get('name')} - {element.get('characteristics', {}).get('personality', '')}")
        
        if polarity:
            lines.append(f"Polarity: {polarity.get('type')} - {polarity.get('meaning', '')}")
        
        return "\n".join(lines)
    
    def _format_tarot_section(self, tarot_data: Dict[str, Any]) -> str:
        """Format tarot data for prompt."""
        if not tarot_data:
            return "No tarot data available."
            
        lines = []
        
        spread = tarot_data.get("spread", {})
        cards = tarot_data.get("cards", [])
        
        if spread:
            lines.append(f"Spread: {spread.get('name')} - {spread.get('description', '')}")
        
        if cards:
            lines.append("Cards Drawn:")
            for card in cards:
                position = card.get("position", {})
                position_name = position.get("name", "Unknown Position")
                card_name = card.get("name", "Unknown Card")
                reversed = " (Reversed)" if card.get("reversed") else ""
                meaning = card.get("upright_meaning" if not card.get("reversed") else "reversed_meaning", "")
                
                lines.append(f"  {position_name}: {card_name}{reversed}")
                if meaning:
                    lines.append(f"    Meaning: {meaning}")
        
        return "\n".join(lines)
