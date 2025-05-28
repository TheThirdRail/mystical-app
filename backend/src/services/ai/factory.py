"""
LLM provider factory for creating provider instances.
"""

from typing import Optional

from src.core.config import settings
from src.core.exceptions import LLMProviderError
from .base import LLMProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .google_provider import GoogleProvider
from .meta_provider import MetaProvider


def get_llm_provider(
    provider_name: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> LLMProvider:
    """
    Get LLM provider instance.
    
    Args:
        provider_name: Name of the provider (openai, anthropic, google, meta)
        api_key: API key for the provider (optional)
        model: Model name (optional)
        
    Returns:
        LLM provider instance
        
    Raises:
        LLMProviderError: If provider is not supported or configuration is invalid
    """
    provider_name = provider_name or settings.DEFAULT_LLM_PROVIDER
    
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "google": GoogleProvider,
        "meta": MetaProvider,
    }
    
    if provider_name not in providers:
        raise LLMProviderError(
            provider_name,
            f"Unsupported provider: {provider_name}. "
            f"Supported providers: {', '.join(providers.keys())}"
        )
    
    provider_class = providers[provider_name]
    
    try:
        provider = provider_class(api_key=api_key, model=model)
        
        if not provider.validate_config():
            raise LLMProviderError(
                provider_name,
                f"Invalid configuration for provider: {provider_name}"
            )
        
        return provider
        
    except Exception as e:
        if isinstance(e, LLMProviderError):
            raise
        raise LLMProviderError(
            provider_name,
            f"Failed to initialize provider: {str(e)}"
        )


def get_available_providers() -> list:
    """Get list of available providers based on configuration."""
    available = []
    
    if settings.OPENAI_API_KEY:
        available.append("openai")
    
    if settings.ANTHROPIC_API_KEY:
        available.append("anthropic")
    
    if settings.GOOGLE_API_KEY:
        available.append("google")
    
    if settings.GPT4FREE_HOST:
        available.append("meta")
    
    return available


def validate_provider_config(provider_name: str) -> bool:
    """Validate if provider configuration is available."""
    config_map = {
        "openai": settings.OPENAI_API_KEY,
        "anthropic": settings.ANTHROPIC_API_KEY,
        "google": settings.GOOGLE_API_KEY,
        "meta": settings.GPT4FREE_HOST,
    }
    
    return bool(config_map.get(provider_name))
