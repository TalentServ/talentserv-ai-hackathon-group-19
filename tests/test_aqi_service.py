"""
Tests for AQI service
"""
import pytest
from unittest.mock import Mock, patch
from services.aqi_service import AQIService


class TestAQIService:
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = AQIService()
    
    @patch('services.aqi_service.requests.get')
    @patch.dict('os.environ', {'OPENWEATHER_API_KEY': 'test_key'})
    def test_get_aqi_success(self, mock_get):
        """Test successful AQI data fetch"""
        # Mock geocoding response
        mock_geo_response = Mock()
        mock_geo_response.json.return_value = [{"lat": 18.5204, "lon": 73.8567}]
        mock_geo_response.raise_for_status = Mock()
        
        # Mock AQI response
        mock_aqi_response = Mock()
        mock_aqi_response.json.return_value = {
            "list": [{
                "main": {"aqi": 2},
                "components": {
                    "pm2_5": 25.3,
                    "pm10": 45.2,
                    "o3": 30.1,
                    "no2": 15.5
                }
            }]
        }
        mock_aqi_response.raise_for_status = Mock()
        
        mock_get.side_effect = [mock_geo_response, mock_aqi_response]
        
        # Call service
        result = self.service.get_aqi("Pune")
        
        # Assertions
        assert result["status"] == "success"
        assert result["location"] == "Pune"
        assert result["aqi_score"] == 40
        assert result["aqi_level"] == "Fair"
        assert result["confidence"] == "high"
    
    @patch('services.aqi_service.requests.get')
    @patch.dict('os.environ', {'OPENWEATHER_API_KEY': 'test_key'})
    def test_get_aqi_location_not_found(self, mock_get):
        """Test handling of location not found"""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = self.service.get_aqi("InvalidCity")
        
        assert result["status"] == "error"
        assert "Location not found" in result["error"]
    
    def test_normalize_response(self):
        """Test AQI response normalization"""
        raw_data = {
            "list": [{
                "main": {"aqi": 3},
                "components": {
                    "pm2_5": 35.5,
                    "pm10": 55.2
                }
            }]
        }
        
        result = self.service._normalize_response(raw_data, "Pune")
        
        assert result["location"] == "Pune"
        assert result["aqi_score"] == 60
        assert result["pollution_level"] == "Moderate"
        assert "timestamp" in result
        assert "source" in result
