"""
Tests for API endpoints.
"""

import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "app" in data
        assert "version" in data


class TestRootEndpoint:
    """Test root endpoint."""
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "MetaMystic" in data["message"]


class TestAstrologyEndpoints:
    """Test astrology API endpoints."""
    
    def test_get_zodiac_signs(self):
        """Test getting zodiac signs information."""
        response = client.get("/api/v1/astro/signs")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "signs" in data["data"]
        assert len(data["data"]["signs"]) == 12
        
        # Check first sign
        aries = data["data"]["signs"][0]
        assert aries["name"] == "Aries"
        assert aries["element"] == "Fire"
        assert aries["modality"] == "Cardinal"
    
    def test_birth_chart_calculation_invalid_data(self):
        """Test birth chart calculation with invalid data."""
        invalid_data = {
            "birth_date": "1990-06-15T00:00:00",
            "birth_time": "25:00",  # Invalid time
            "birth_location": "New York",
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        
        response = client.post("/api/v1/astro/chart", json=invalid_data)
        assert response.status_code == 422  # Validation error


class TestNumerologyEndpoints:
    """Test numerology API endpoints."""
    
    def test_life_path_calculation(self):
        """Test life path number calculation."""
        birth_date = "1990-06-15T00:00:00"
        
        response = client.post(f"/api/v1/numerology/life-path?birth_date={birth_date}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "number" in data["data"]
        assert "calculation" in data["data"]
        assert "meaning" in data["data"]
    
    def test_expression_calculation(self):
        """Test expression number calculation."""
        response = client.post("/api/v1/numerology/expression?full_name=John Doe")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "number" in data["data"]
    
    def test_get_number_meanings(self):
        """Test getting number meanings."""
        response = client.get("/api/v1/numerology/meanings")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "meanings" in data["data"]
        assert "1" in data["data"]["meanings"]
        assert "11" in data["data"]["meanings"]  # Master number


class TestChineseZodiacEndpoints:
    """Test Chinese zodiac API endpoints."""
    
    def test_zodiac_calculation(self):
        """Test Chinese zodiac calculation."""
        request_data = {
            "birth_date": "1990-06-15T00:00:00"
        }
        
        response = client.post("/api/v1/zodiac/calculate", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "animal" in data["data"]
        assert "element" in data["data"]
        assert "polarity" in data["data"]
    
    def test_get_zodiac_animals(self):
        """Test getting zodiac animals information."""
        response = client.get("/api/v1/zodiac/animals")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "animals" in data["data"]
        assert len(data["data"]["animals"]) == 6  # We only defined 6 animals in the endpoint
    
    def test_get_zodiac_elements(self):
        """Test getting zodiac elements information."""
        response = client.get("/api/v1/zodiac/elements")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "elements" in data["data"]
        assert len(data["data"]["elements"]) == 5
    
    def test_compatibility_check(self):
        """Test zodiac compatibility check."""
        response = client.get("/api/v1/zodiac/compatibility/Rat/Dragon")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "compatibility" in data["data"]
        assert data["data"]["animal1"] == "Rat"
        assert data["data"]["animal2"] == "Dragon"


class TestTarotEndpoints:
    """Test tarot API endpoints."""
    
    def test_get_spreads(self):
        """Test getting tarot spreads."""
        response = client.get("/api/v1/tarot/spreads")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "spreads" in data["data"]
    
    def test_get_specific_spread(self):
        """Test getting specific spread."""
        response = client.get("/api/v1/tarot/spreads/three_card")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["slug"] == "three_card"
        assert data["data"]["card_count"] == 3
    
    def test_get_decks(self):
        """Test getting tarot decks."""
        response = client.get("/api/v1/tarot/decks")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "decks" in data["data"]
    
    def test_get_major_arcana(self):
        """Test getting Major Arcana cards."""
        response = client.get("/api/v1/tarot/cards/major-arcana")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "cards" in data["data"]
        assert data["data"]["count"] == 22  # 22 Major Arcana cards
    
    def test_card_interpretation(self):
        """Test card interpretation."""
        response = client.post("/api/v1/tarot/interpret?card_name=The Fool&reversed=false")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "card_name" in data["data"]
        assert data["data"]["card_name"] == "The Fool"
    
    def test_tarot_draw(self):
        """Test tarot card drawing."""
        request_data = {
            "spread_slug": "one_card",
            "seed": 12345  # For reproducible results
        }
        
        response = client.post("/api/v1/tarot/draw", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "cards" in data["data"]
        assert len(data["data"]["cards"]) == 1  # One card spread


class TestPartnerEndpoints:
    """Test partner API endpoints."""
    
    def test_list_partners(self):
        """Test listing partners."""
        response = client.get("/api/v1/partners/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_partner(self):
        """Test getting specific partner."""
        response = client.get("/api/v1/partners/metamystic")
        assert response.status_code == 200
        data = response.json()
        assert data["slug"] == "metamystic"
        assert data["name"] == "MetaMystic"
    
    def test_get_partner_personas(self):
        """Test getting partner personas."""
        response = client.get("/api/v1/partners/metamystic/personas")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_public_partners(self):
        """Test getting public partner information."""
        response = client.get("/api/v1/partners/public")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "partners" in data["data"]


class TestAuthEndpoints:
    """Test authentication endpoints."""
    
    def test_login_endpoint(self):
        """Test login endpoint (mock)."""
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_register_endpoint(self):
        """Test registration endpoint (mock)."""
        register_data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "full_name": "New User"
        }
        
        response = client.post("/api/v1/auth/register", json=register_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
