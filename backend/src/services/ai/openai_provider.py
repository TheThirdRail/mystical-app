"""
OpenAI LLM provider implementation.
"""

import asyncio
from typing import Dict, Any, Optional

import openai
from openai import AsyncOpenAI

from src.core.config import settings
from src.core.exceptions import LLMProviderError
from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__(
            api_key=api_key or settings.OPENAI_API_KEY,
            model=model or settings.OPENAI_MODEL
        )
        
        if not self.api_key:
            raise LLMProviderError("openai", "API key not provided")
            
        self.client = AsyncOpenAI(api_key=self.api_key)
    
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using OpenAI API."""
        try:
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                # Default system prompt for spiritual readings
                default_system = (
                    "You are a wise and compassionate spiritual guide. "
                    "Provide insightful, positive, and empowering readings. "
                    "Always frame challenges as opportunities for growth. "
                    "Be specific but avoid making absolute predictions about the future. "
                    "Focus on guidance and personal empowerment."
                )
                messages.append({"role": "system", "content": default_system})
            
            # Add user prompt
            messages.append({"role": "user", "content": prompt})
            
            # Make API call
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens or 1500,
                **kwargs
            )
            
            # Extract response data
            choice = response.choices[0]
            content = choice.message.content
            
            return {
                "content": content,
                "provider": self.get_provider_name(),
                "model": self.get_model_name(),
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
                "finish_reason": choice.finish_reason,
                "metadata": {
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
            }
            
        except openai.APIError as e:
            raise LLMProviderError("openai", f"API error: {str(e)}")
        except openai.RateLimitError as e:
            raise LLMProviderError("openai", f"Rate limit exceeded: {str(e)}")
        except openai.AuthenticationError as e:
            raise LLMProviderError("openai", f"Authentication failed: {str(e)}")
        except Exception as e:
            raise LLMProviderError("openai", f"Unexpected error: {str(e)}")
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "openai"
    
    def get_model_name(self) -> str:
        """Get model name."""
        return self.model
    
    def validate_config(self) -> bool:
        """Validate OpenAI configuration."""
        return bool(self.api_key and self.model)
