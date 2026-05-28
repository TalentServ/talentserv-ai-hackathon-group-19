"""
Tests for recommendation service
"""
import pytest
from services.recommendation_service import RecommendationService


class TestRecommendationService:
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = RecommendationService()
        
        # Sample weather data
        self.weather_data = {
            "location": "Pune",
            "temperature": 28.5,
            "humidity": 65,
            "wind_speed": 3.5,
            "rain_probability": 30,
            "weather_condition": "Clear",
            "status": "success"
        }
        
        # Sample AQI data
        self.aqi_data = {
            "location": "Pune",
            "aqi_score": 40,
            "aqi_level": "Fair",
            "pollution_level": "Fair",
            "health_warning": "Air quality is acceptable",
            "status": "success"
        }
        
        # Sample places data
        self.places_data = {
            "location": "Pune",
            "total_places": 15,
            "places": [
                {"name": "Place 1", "category": "Tourist Attraction", "distance": 500},
                {"name": "Place 2", "category": "Museum", "distance": 1000},
            ],
            "status": "success"
        }
    
    def test_generate_recommendation_success(self):
        """Test successful recommendation generation"""
        result = self.service.generate_recommendation(
            self.weather_data, self.aqi_data, self.places_data
        )
        
        assert result["status"] == "success"
        assert result["location"] == "Pune"
        assert "confidence_score" in result
        assert "recommendation" in result
        assert "travel_advice" in result
        assert isinstance(result["travel_advice"], list)
    
    def test_calculate_weather_score(self):
        """Test weather score calculation"""
        score = self.service._calculate_weather_score(self.weather_data)
        
        assert 0 <= score <= 100
        assert score > 50  # Should be favorable
    
    def test_calculate_weather_score_high_temp(self):
        """Test weather score with high temperature"""
        hot_weather = self.weather_data.copy()
        hot_weather["temperature"] = 38
        
        score = self.service._calculate_weather_score(hot_weather)
        
        assert score < 75  # Should be penalized
    
    def test_calculate_aqi_score(self):
        """Test AQI score calculation"""
        score = self.service._calculate_aqi_score(self.aqi_data)
        
        assert 0 <= score <= 100
        assert score == 80  # Fair AQI (40) should give 80 points
    
    def test_calculate_places_score(self):
        """Test places score calculation"""
        score = self.service._calculate_places_score(self.places_data)
        
        assert 0 <= score <= 100
        assert score == 100  # 15 places should give max score
    
    def test_generate_shopping_list(self):
        """Test shopping list generation"""
        result = self.service.generate_shopping_list(
            self.weather_data, self.aqi_data
        )
        
        assert result["status"] == "success"
        assert "items" in result
        assert isinstance(result["items"], list)
        assert result["total_items"] > 0
        
        # Check item structure
        if result["items"]:
            item = result["items"][0]
            assert "item" in item
            assert "reason" in item
            assert "priority" in item
    
    def test_confidence_levels(self):
        """Test confidence level mapping"""
        assert self.service._get_confidence_level(85) == "Very High"
        assert self.service._get_confidence_level(70) == "High"
        assert self.service._get_confidence_level(50) == "Moderate"
        assert self.service._get_confidence_level(30) == "Low"
    
    def test_recommendation_with_error_data(self):
        """Test recommendation with error in data sources"""
        error_weather = {"status": "error", "location": "Pune"}
        
        result = self.service.generate_recommendation(
            error_weather, self.aqi_data, self.places_data
        )
        
        # Should still generate a recommendation
        assert result["status"] == "success"
        assert "confidence_score" in result
