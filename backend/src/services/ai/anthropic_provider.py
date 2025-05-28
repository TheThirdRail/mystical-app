"""
Anthropic LLM provider implementation.
"""

from typing import Dict, Any, Optional

import anthropic
from anthropic import AsyncAnthropic

from src.core.config import settings
from src.core.exceptions import LLMProviderError
from .base import LLMProvider


class AnthropicProvider(LLMProvider):
    """Anthropic LLM provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__(
            api_key=api_key or settings.ANTHROPIC_API_KEY,
            model=model or settings.ANTHROPIC_MODEL
        )
        
        if not self.api_key:
            raise LLMProviderError("anthropic", "API key not provided")
            
        self.client = AsyncAnthropic(api_key=self.api_key)
    
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using Anthropic API."""
        try:
            # Default system prompt for spiritual readings
            if not system_prompt:
                system_prompt = (
                    "You are a wise and compassionate spiritual guide. "
                    "Provide insightful, positive, and empowering readings. "
                    "Always frame challenges as opportunities for growth. "
                    "Be specific but avoid making absolute predictions about the future. "
                    "Focus on guidance and personal empowerment."
                )
            
            # Make API call
            response = await self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens or 1500,
                **kwargs
            )
            
            # Extract response data
            content = response.content[0].text
            
            return {
                "content": content,
                "provider": self.get_provider_name(),
                "model": self.get_model_name(),
                "usage": {
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
                },
                "finish_reason": response.stop_reason,
                "metadata": {
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
            }
            
        except anthropic.APIError as e:
            raise LLMProviderError("anthropic", f"API error: {str(e)}")
        except anthropic.RateLimitError as e:
            raise LLMProviderError("anthropic", f"Rate limit exceeded: {str(e)}")
        except anthropic.AuthenticationError as e:
            raise LLMProviderError("anthropic", f"Authentication failed: {str(e)}")
        except Exception as e:
            raise LLMProviderError("anthropic", f"Unexpected error: {str(e)}")
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "anthropic"
    
    def get_model_name(self) -> str:
        """Get model name."""
        return self.model
    
    def validate_config(self) -> bool:
        """Validate Anthropic configuration."""
        return bool(self.api_key and self.model)
