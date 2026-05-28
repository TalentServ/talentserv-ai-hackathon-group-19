"""
Tests for utilities
"""
import pytest
from utils.markdown_generator import MarkdownTableGenerator
from utils.confidence_calculator import ConfidenceCalculator
from utils.response_normalizer import ResponseNormalizer


class TestMarkdownTableGenerator:
    
    def test_generate_weather_table(self):
        """Test weather table generation"""
        weather_data = {
            "temperature": 28.5,
            "humidity": 65,
            "wind_speed": 3.5,
            "rain_probability": 30,
            "weather_condition": "Clear",
            "source": "OpenWeatherMap",
            "confidence": "high"
        }
        
        table = MarkdownTableGenerator.generate_weather_table(weather_data)
        
        assert "| Metric" in table
        assert "| Temperature" in table
        assert "28.5" in table
        assert "|" in table
    
    def test_generate_shopping_table(self):
        """Test shopping table generation"""
        shopping_list = {
            "items": [
                {"item": "Umbrella", "reason": "Rain expected", "priority": "high"},
                {"item": "Sunscreen", "reason": "High UV", "priority": "medium"}
            ]
        }
        
        table = MarkdownTableGenerator.generate_shopping_table(shopping_list)
        
        assert "Umbrella" in table
        assert "Sunscreen" in table
        assert "HIGH" in table


class TestConfidenceCalculator:
    
    def test_calculate_overall_confidence(self):
        """Test overall confidence calculation"""
        scores = [80, 70, 90]
        result = ConfidenceCalculator.calculate_overall_confidence(scores)
        
        assert result == 80.0  # Average
    
    def test_calculate_weighted_confidence(self):
        """Test weighted confidence calculation"""
        scores = [80, 60, 70]
        weights = [0.5, 0.3, 0.2]
        
        result = ConfidenceCalculator.calculate_overall_confidence(scores, weights)
        
        expected = (80 * 0.5) + (60 * 0.3) + (70 * 0.2)
        assert result == round(expected, 2)
    
    def test_get_confidence_level(self):
        """Test confidence level mapping"""
        assert ConfidenceCalculator.get_confidence_level(85) == "Very High"
        assert ConfidenceCalculator.get_confidence_level(65) == "High"
        assert ConfidenceCalculator.get_confidence_level(45) == "Moderate"
        assert ConfidenceCalculator.get_confidence_level(25) == "Low"
        assert ConfidenceCalculator.get_confidence_level(10) == "Very Low"
    
    def test_invalid_weights(self):
        """Test error handling for invalid weights"""
        scores = [80, 70]
        weights = [0.5, 0.3]  # Don't sum to 1.0
        
        with pytest.raises(ValueError):
            ConfidenceCalculator.calculate_overall_confidence(scores, weights)


class TestResponseNormalizer:
    
    def test_normalize_response(self):
        """Test response normalization"""
        data = {
            "temperature": 28.5,
            "location": "Pune"
        }
        
        result = ResponseNormalizer.normalize_response(data, "TestSource", "success")
        
        assert result["temperature"] == 28.5
        assert result["location"] == "Pune"
        assert result["source"] == "TestSource"
        assert result["status"] == "success"
        assert "timestamp" in result
        assert "confidence" in result
    
    def test_normalize_error_response(self):
        """Test error response normalization"""
        result = ResponseNormalizer.normalize_error_response(
            "API timeout", "TestSource", "Pune"
        )
        
        assert result["status"] == "error"
        assert result["error"] == "API timeout"
        assert result["source"] == "TestSource"
        assert result["location"] == "Pune"
        assert "timestamp" in result
    
    def test_normalize_list_response(self):
        """Test list response normalization"""
        items = [{"name": "Place 1"}, {"name": "Place 2"}]
        
        result = ResponseNormalizer.normalize_list_response(
            items, "TestSource", "Pune"
        )
        
        assert result["items"] == items
        assert result["total_count"] == 2
        assert result["location"] == "Pune"
        assert result["status"] == "success"
