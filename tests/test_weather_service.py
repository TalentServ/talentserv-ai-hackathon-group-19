"""
Tests for weather service
"""
import pytest
from unittest.mock import Mock, patch
from services.weather_service import WeatherService


class TestWeatherService:
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = WeatherService()
    
    @patch('services.weather_service.requests.get')
    @patch.dict('os.environ', {'OPENWEATHER_API_KEY': 'test_key'})
    def test_get_weather_success(self, mock_get):
        """Test successful weather data fetch"""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "name": "Pune",
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "main": {"temp": 28.5, "feels_like": 30.2, "humidity": 65},
            "wind": {"speed": 3.5},
            "rain": {}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Call service
        result = self.service.get_weather("Pune")
        
        # Assertions
        assert result["status"] == "success"
        assert result["location"] == "Pune"
        assert result["temperature"] == 28.5
        assert result["humidity"] == 65
        assert result["confidence"] == "high"
    
    @patch('services.weather_service.requests.get')
    @patch.dict('os.environ', {'OPENWEATHER_API_KEY': 'test_key'})
    def test_get_weather_timeout(self, mock_get):
        """Test weather service timeout handling"""
        mock_get.side_effect = Exception("Timeout")
        
        result = self.service.get_weather("Pune")
        
        assert result["status"] == "error"
        assert "error" in result
    
    @patch.dict('os.environ', {}, clear=True)
    def test_get_weather_missing_api_key(self):
        """Test handling of missing API key"""
        service = WeatherService()
        result = service.get_weather("Pune")
        
        assert result["status"] == "error"
        assert "Missing API key" in result["error"]
    
    def test_normalize_response(self):
        """Test response normalization"""
        raw_data = {
            "name": "Pune",
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "main": {"temp": 28.5, "feels_like": 30.2, "humidity": 65},
            "wind": {"speed": 3.5},
            "rain": {}
        }
        
        result = self.service._normalize_response(raw_data)
        
        assert "timestamp" in result
        assert "source" in result
        assert result["source"] == "OpenWeatherMap"
        assert "confidence" in result
