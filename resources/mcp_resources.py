"""
MCP Resources - Provide context and reference data to AI agents
"""
from typing import Dict, Any


class MCPResources:
    
    @staticmethod
    def get_recommendation_rules() -> Dict[str, Any]:
        """Get recommendation generation rules and guidelines"""
        return {
            "title": "Recommendation Rules",
            "description": "Guidelines for generating travel recommendations",
            "rules": {
                "weather_scoring": {
                    "ideal_temperature_range": "20-28°C",
                    "high_temperature_penalty": "> 35°C: -30 points",
                    "low_temperature_penalty": "< 15°C: -30 points",
                    "rain_penalty": "> 70%: -30 points, > 40%: -15 points",
                    "wind_penalty": "> 20 m/s: -20 points, > 15 m/s: -10 points"
                },
                "aqi_scoring": {
                    "good": "0-20: 100 points",
                    "fair": "21-40: 80 points",
                    "moderate": "41-60: 60 points",
                    "poor": "61-80: 40 points",
                    "very_poor": "81-100: 20 points"
                },
                "places_scoring": {
                    "excellent": "15+ places: 100 points",
                    "good": "10-14 places: 80 points",
                    "moderate": "5-9 places: 60 points",
                    "fair": "2-4 places: 40 points",
                    "poor": "0-1 places: 20 points"
                },
                "confidence_levels": {
                    "very_high": "80-100%",
                    "high": "60-79%",
                    "moderate": "40-59%",
                    "low": "0-39%"
                },
                "recommendation_thresholds": {
                    "should_visit": ">= 60% confidence",
                    "consider_visit": "40-59% confidence",
                    "not_recommended": "< 40% confidence"
                }
            },
            "metadata": {
                "version": "1.0",
                "last_updated": "2024-01-01"
            }
        }
    
    @staticmethod
    def get_supported_locations() -> Dict[str, Any]:
        """Get list of popular supported locations"""
        return {
            "title": "Supported Locations",
            "description": "Popular cities and regions with comprehensive data coverage",
            "locations": {
                "india": [
                    "Mumbai, IN",
                    "Delhi, IN",
                    "Bangalore, IN",
                    "Pune, IN",
                    "Chennai, IN",
                    "Kolkata, IN",
                    "Hyderabad, IN",
                    "Ahmedabad, IN",
                    "Jaipur, IN",
                    "Goa, IN"
                ],
                "international": [
                    "New York, US",
                    "London, UK",
                    "Paris, FR",
                    "Tokyo, JP",
                    "Dubai, AE",
                    "Singapore, SG",
                    "Sydney, AU",
                    "Barcelona, ES",
                    "Rome, IT",
                    "Bangkok, TH"
                ]
            },
            "notes": [
                "Any city name can be used, these are just popular examples",
                "Use format: 'City, Country Code' for better accuracy",
                "Country codes are ISO 3166-1 alpha-2 codes"
            ],
            "metadata": {
                "total_supported": "All major cities worldwide",
                "api_coverage": "Global"
            }
        }
    
    @staticmethod
    def get_tourist_categories() -> Dict[str, Any]:
        """Get tourist place categories and descriptions"""
        return {
            "title": "Tourist Place Categories",
            "description": "Categories of places returned by the Places API",
            "categories": {
                "tourist_attractions": {
                    "description": "Popular tourist destinations and landmarks",
                    "examples": ["monuments", "landmarks", "viewpoints", "heritage sites"],
                    "api_category": "tourism.attraction"
                },
                "museums": {
                    "description": "Museums and cultural centers",
                    "examples": ["art museums", "history museums", "science centers", "galleries"],
                    "api_category": "entertainment.museum"
                },
                "parks": {
                    "description": "Parks and outdoor recreational areas",
                    "examples": ["city parks", "gardens", "nature reserves", "playgrounds"],
                    "api_category": "leisure.park"
                },
                "restaurants": {
                    "description": "Dining establishments and cafes",
                    "examples": ["restaurants", "cafes", "food courts", "eateries"],
                    "api_category": "catering.restaurant"
                }
            },
            "search_parameters": {
                "default_radius": "5000 meters (5 km)",
                "max_results_per_category": 10,
                "total_max_results": 20
            },
            "metadata": {
                "data_provider": "Geoapify Places API",
                "update_frequency": "Real-time"
            }
        }
    
    @staticmethod
    def get_sample_outputs() -> Dict[str, Any]:
        """Get sample output formats and examples"""
        return {
            "title": "Sample Outputs",
            "description": "Example responses from different MCP tools",
            "examples": {
                "weather_response": {
                    "location": "Pune",
                    "temperature": 28.5,
                    "feels_like": 30.2,
                    "humidity": 65,
                    "wind_speed": 3.5,
                    "rain_probability": 30,
                    "weather_condition": "Clouds",
                    "description": "scattered clouds",
                    "source": "OpenWeatherMap",
                    "confidence": "high",
                    "status": "success"
                },
                "aqi_response": {
                    "location": "Pune",
                    "aqi_score": 60,
                    "pollution_level": "Moderate",
                    "health_warning": "Sensitive groups may experience issues",
                    "pm2_5": 25.3,
                    "pm10": 45.2,
                    "source": "OpenWeatherMap Air Pollution API",
                    "confidence": "high",
                    "status": "success"
                },
                "recommendation_response": {
                    "location": "Pune",
                    "recommendation": "Good time to visit Pune. Weather and air quality are favorable.",
                    "should_visit": True,
                    "confidence_score": 72.5,
                    "confidence_level": "High",
                    "travel_advice": [
                        "Stay hydrated and wear light clothing",
                        "Enjoy your visit!"
                    ],
                    "weather_score": 75.0,
                    "aqi_score": 60.0,
                    "places_score": 82.0,
                    "status": "success"
                },
                "shopping_list_response": {
                    "location": "Pune",
                    "items": [
                        {
                            "item": "Water Bottle",
                            "reason": "Stay hydrated in warm weather",
                            "priority": "high"
                        },
                        {
                            "item": "Sunscreen",
                            "reason": "High temperature (28.5°C)",
                            "priority": "high"
                        }
                    ],
                    "total_items": 2,
                    "status": "success"
                }
            },
            "markdown_table_example": """
| Metric | Value | Source |
| ------ | ----- | ------ |
| Temperature | 28.5°C | OpenWeatherMap |
| Humidity | 65% | |
| Rain Probability | 30% | |
"""
        }
    
    @staticmethod
    def get_all_resources() -> Dict[str, Any]:
        """Get all resources in a single response"""
        return {
            "recommendation_rules": MCPResources.get_recommendation_rules(),
            "supported_locations": MCPResources.get_supported_locations(),
            "tourist_categories": MCPResources.get_tourist_categories(),
            "sample_outputs": MCPResources.get_sample_outputs()
        }
