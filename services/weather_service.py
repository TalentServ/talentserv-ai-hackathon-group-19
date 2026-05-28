"""
Weather service for fetching weather data from OpenWeatherMap API
"""
import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime


class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
    def get_weather(self, location: str) -> Dict[str, Any]:
        """
        Fetch weather data for a given location
        
        Args:
            location: City name (e.g., "Pune", "Mumbai, IN")
            
        Returns:
            Normalized weather data with metadata
        """
        if not self.api_key:
            return self._get_fallback_response(location, "Missing API key")
        
        # Validate location input
        if not location or len(location.strip()) < 2:
            return self._get_fallback_response(location, "Invalid city name. Please enter a valid city.")
            
        try:
            params = {
                "q": location.strip(),
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            # Check if city was found
            if response.status_code == 404:
                return self._get_fallback_response(location, f"City '{location}' not found. Please enter a correct city name.")
            
            response.raise_for_status()
            data = response.json()
            
            # Double check if we got valid data
            if not data.get("name"):
                return self._get_fallback_response(location, f"City '{location}' not found. Please enter a correct city name.")
            
            return self._normalize_response(data)
            
        except requests.exceptions.Timeout:
            return self._get_fallback_response(location, "API timeout")
        except requests.exceptions.RequestException as e:
            if "404" in str(e):
                return self._get_fallback_response(location, f"City '{location}' not found. Please enter a correct city name.")
            return self._get_fallback_response(location, f"API error: {str(e)}")
        except Exception as e:
            return self._get_fallback_response(location, f"Unexpected error: {str(e)}")
    
    def _normalize_response(self, data: Dict) -> Dict[str, Any]:
        """Normalize API response to standard format"""
        weather = data.get("weather", [{}])[0]
        main = data.get("main", {})
        wind = data.get("wind", {})
        rain = data.get("rain", {})
        
        rain_probability = 0
        if rain.get("1h", 0) > 0:
            rain_probability = min(100, int(rain.get("1h", 0) * 10))
        elif weather.get("main", "").lower() in ["rain", "drizzle"]:
            rain_probability = 70
        elif "cloud" in weather.get("main", "").lower():
            rain_probability = 30
            
        return {
            "location": data.get("name", "Unknown"),
            "temperature": round(main.get("temp", 0), 1),
            "feels_like": round(main.get("feels_like", 0), 1),
            "humidity": main.get("humidity", 0),
            "wind_speed": round(wind.get("speed", 0), 1),
            "rain_probability": rain_probability,
            "weather_condition": weather.get("main", "Unknown"),
            "description": weather.get("description", ""),
            "timestamp": datetime.utcnow().isoformat(),
            "source": "OpenWeatherMap",
            "confidence": "high",
            "status": "success"
        }
    
    def _get_fallback_response(self, location: str, error: str) -> Dict[str, Any]:
        """Return fallback response on error"""
        return {
            "location": location,
            "temperature": None,
            "feels_like": None,
            "humidity": None,
            "wind_speed": None,
            "rain_probability": None,
            "weather_condition": "Unknown",
            "description": "",
            "timestamp": datetime.utcnow().isoformat(),
            "source": "OpenWeatherMap",
            "confidence": "none",
            "status": "error",
            "error": error
        }
