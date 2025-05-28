"""
Tests for service layer components.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from src.services.ai.base import LLMProvider
from src.services.ai.openai_provider import OpenAIProvider
from src.services.ai.factory import get_llm_provider, get_available_providers
from src.core.exceptions import LLMProviderError


class TestLLMProviderBase:
    """Test base LLM provider functionality."""
    
    def test_format_reading_prompt(self):
        """Test reading prompt formatting."""
        # Create a mock provider
        provider = Mock(spec=LLMProvider)
        provider.format_reading_prompt = LLMProvider.format_reading_prompt.__get__(provider)
        
        # Mock data
        astro_data = {
            "birth_info": {"date": "1990-06-15", "location": "New York"},
            "planets": {"Sun": {"sign": "Gemini", "house": 1}},
            "elements": {"air": 3, "fire": 2, "earth": 2, "water": 1}
        }
        
        numerology_data = {
            "core_numbers": {
                "life_path": {"number": 7, "meaning": "Spirituality and introspection"}
            }
        }
        
        zodiac_data = {
            "animal": {"name": "Horse", "traits": {"personality": "Free-spirited"}},
            "element": {"name": "Metal", "characteristics": {"personality": "Organized"}}
        }
        
        tarot_data = {
            "spread": {"name": "Three Card", "description": "Past, Present, Future"},
            "cards": [
                {"name": "The Fool", "position": {"name": "Past"}, "reversed": False}
            ]
        }
        
        prompt = provider.format_reading_prompt(
            astro_data=astro_data,
            numerology_data=numerology_data,
            zodiac_data=zodiac_data,
            tarot_data=tarot_data,
            question="What should I focus on?",
            partner_prompt_stub="You are a wise guide.",
            persona_config={"voice_style": "mystical", "tone": "gentle"}
        )
        
        assert isinstance(prompt, str)
        assert "You are a wise guide." in prompt
        assert "mystical" in prompt
        assert "gentle" in prompt
        assert "What should I focus on?" in prompt
        assert "ASTROLOGY:" in prompt
        assert "NUMEROLOGY:" in prompt
        assert "CHINESE ZODIAC:" in prompt
        assert "TAROT:" in prompt


class TestLLMProviderFactory:
    """Test LLM provider factory."""
    
    def test_get_available_providers_no_keys(self):
        """Test getting available providers when no API keys are set."""
        with patch('src.services.ai.factory.settings') as mock_settings:
            mock_settings.OPENAI_API_KEY = None
            mock_settings.ANTHROPIC_API_KEY = None
            mock_settings.GOOGLE_API_KEY = None
            mock_settings.GPT4FREE_HOST = None
            
            providers = get_available_providers()
            assert providers == []
    
    def test_get_available_providers_with_keys(self):
        """Test getting available providers when API keys are set."""
        with patch('src.services.ai.factory.settings') as mock_settings:
            mock_settings.OPENAI_API_KEY = "test_key"
            mock_settings.ANTHROPIC_API_KEY = "test_key"
            mock_settings.GOOGLE_API_KEY = None
            mock_settings.GPT4FREE_HOST = None
            
            providers = get_available_providers()
            assert "openai" in providers
            assert "anthropic" in providers
            assert "google" not in providers
            assert "meta" not in providers
    
    def test_get_llm_provider_invalid(self):
        """Test getting invalid LLM provider."""
        with pytest.raises(LLMProviderError):
            get_llm_provider("invalid_provider")
    
    @patch('src.services.ai.factory.settings')
    def test_get_openai_provider(self, mock_settings):
        """Test getting OpenAI provider."""
        mock_settings.OPENAI_API_KEY = "test_key"
        mock_settings.OPENAI_MODEL = "gpt-4"
        
        with patch('src.services.ai.openai_provider.AsyncOpenAI'):
            provider = get_llm_provider("openai")
            assert isinstance(provider, OpenAIProvider)
            assert provider.get_provider_name() == "openai"


class TestOpenAIProvider:
    """Test OpenAI provider implementation."""
    
    def test_provider_initialization_no_key(self):
        """Test provider initialization without API key."""
        with pytest.raises(LLMProviderError):
            OpenAIProvider(api_key=None)
    
    @patch('src.services.ai.openai_provider.AsyncOpenAI')
    def test_provider_initialization_with_key(self, mock_client):
        """Test provider initialization with API key."""
        provider = OpenAIProvider(api_key="test_key", model="gpt-4")
        assert provider.api_key == "test_key"
        assert provider.model == "gpt-4"
        assert provider.get_provider_name() == "openai"
        assert provider.get_model_name() == "gpt-4"
    
    @patch('src.services.ai.openai_provider.AsyncOpenAI')
    async def test_generate_response_success(self, mock_client_class):
        """Test successful response generation."""
        # Mock the OpenAI client and response
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_response.choices[0].finish_reason = "stop"
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5
        mock_response.usage.total_tokens = 15
        
        mock_client.chat.completions.create.return_value = mock_response
        
        provider = OpenAIProvider(api_key="test_key")
        
        result = await provider.generate_response("Test prompt")
        
        assert result["content"] == "Test response"
        assert result["provider"] == "openai"
        assert result["usage"]["total_tokens"] == 15
        assert result["finish_reason"] == "stop"
    
    def test_validate_config_valid(self):
        """Test configuration validation with valid config."""
        with patch('src.services.ai.openai_provider.AsyncOpenAI'):
            provider = OpenAIProvider(api_key="test_key", model="gpt-4")
            assert provider.validate_config() is True
    
    def test_validate_config_invalid(self):
        """Test configuration validation with invalid config."""
        with patch('src.services.ai.openai_provider.AsyncOpenAI'):
            provider = OpenAIProvider(api_key="test_key", model="gpt-4")
            provider.api_key = None
            assert provider.validate_config() is False


class TestReadingService:
    """Test reading service functionality."""
    
    @pytest.fixture
    def mock_db(self):
        """Mock database session."""
        return AsyncMock()
    
    def test_reading_service_initialization(self, mock_db):
        """Test reading service initialization."""
        from src.services.reading_service import ReadingService
        
        service = ReadingService(mock_db)
        assert service.db == mock_db
    
    async def test_perform_calculations_basic(self, mock_db):
        """Test basic calculations performance."""
        from src.services.reading_service import ReadingService
        from src.models.reading import Reading
        
        service = ReadingService(mock_db)
        
        # Create a mock reading
        reading = Reading(
            birth_date=datetime(1990, 6, 15),
            birth_time="14:30",
            birth_location="New York",
            birth_latitude=40.7128,
            birth_longitude=-74.0060,
            question="Test question"
        )
        
        # Mock the calculation methods to avoid external dependencies
        with patch.object(service, '_perform_calculations') as mock_calc:
            mock_calc.return_value = {
                "astrology": {"test": "data"},
                "numerology": {"test": "data"},
                "zodiac": {"test": "data"},
                "tarot": {"test": "data"}
            }
            
            result = await service._perform_calculations(reading)
            
            assert "astrology" in result
            assert "numerology" in result
            assert "zodiac" in result
            assert "tarot" in result
