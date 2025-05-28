"""
Meta LLM provider implementation via GPT4Free or direct API.
"""

from typing import Dict, Any, Optional
import httpx

from src.core.config import settings
from src.core.exceptions import LLMProviderError
from .base import LLMProvider


class MetaProvider(LLMProvider):
    """Meta LLM provider via GPT4Free or direct API."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__(
            api_key=api_key,  # May not be needed for GPT4Free
            model=model or settings.META_MODEL
        )
        
        self.gpt4free_host = settings.GPT4FREE_HOST
        
        if not self.gpt4free_host:
            raise LLMProviderError("meta", "GPT4Free host not configured")
    
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using Meta LLM via GPT4Free."""
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
            
            # Prepare request payload
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens or 1500,
                **kwargs
            }
            
            # Make API call to GPT4Free
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.gpt4free_host}/v1/chat/completions",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                
                data = response.json()
            
            # Extract response data
            if "choices" not in data or not data["choices"]:
                raise LLMProviderError("meta", "No response choices returned")
            
            choice = data["choices"][0]
            content = choice["message"]["content"]
            
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
                "finish_reason": choice.get("finish_reason", "unknown"),
                "metadata": {
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "gpt4free_host": self.gpt4free_host,
                }
            }
            
        except httpx.HTTPError as e:
            raise LLMProviderError("meta", f"HTTP error: {str(e)}")
        except httpx.TimeoutException as e:
            raise LLMProviderError("meta", f"Request timeout: {str(e)}")
        except Exception as e:
            raise LLMProviderError("meta", f"Unexpected error: {str(e)}")
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "meta"
    
    def get_model_name(self) -> str:
        """Get model name."""
        return self.model
    
    def validate_config(self) -> bool:
        """Validate Meta configuration."""
        return bool(self.gpt4free_host and self.model)
