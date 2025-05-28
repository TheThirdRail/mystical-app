"""
Google Generative AI provider implementation.
"""

from typing import Dict, Any, Optional

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from src.core.config import settings
from src.core.exceptions import LLMProviderError
from .base import LLMProvider


class GoogleProvider(LLMProvider):
    """Google Generative AI provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__(
            api_key=api_key or settings.GOOGLE_API_KEY,
            model=model or settings.GOOGLE_MODEL
        )
        
        if not self.api_key:
            raise LLMProviderError("google", "API key not provided")
            
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(self.model)
    
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using Google Generative AI."""
        try:
            # Combine system prompt with user prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            else:
                # Default system prompt for spiritual readings
                default_system = (
                    "You are a wise and compassionate spiritual guide. "
                    "Provide insightful, positive, and empowering readings. "
                    "Always frame challenges as opportunities for growth. "
                    "Be specific but avoid making absolute predictions about the future. "
                    "Focus on guidance and personal empowerment."
                )
                full_prompt = f"{default_system}\n\n{prompt}"
            
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens or 1500,
                **kwargs
            )
            
            # Configure safety settings to be less restrictive for spiritual content
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            
            # Make API call
            response = await self.client.generate_content_async(
                full_prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Extract response data
            content = response.text
            
            # Calculate token usage (approximate)
            prompt_tokens = len(full_prompt.split()) * 1.3  # Rough estimate
            completion_tokens = len(content.split()) * 1.3
            
            return {
                "content": content,
                "provider": self.get_provider_name(),
                "model": self.get_model_name(),
                "usage": {
                    "prompt_tokens": int(prompt_tokens),
                    "completion_tokens": int(completion_tokens),
                    "total_tokens": int(prompt_tokens + completion_tokens),
                },
                "finish_reason": response.candidates[0].finish_reason.name if response.candidates else "unknown",
                "metadata": {
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
            }
            
        except Exception as e:
            raise LLMProviderError("google", f"API error: {str(e)}")
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "google"
    
    def get_model_name(self) -> str:
        """Get model name."""
        return self.model
    
    def validate_config(self) -> bool:
        """Validate Google configuration."""
        return bool(self.api_key and self.model)
