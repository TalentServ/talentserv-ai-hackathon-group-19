"""
AQI (Air Quality Index) service for fetching pollution data from OpenWeatherMap API
"""
import os
import requests
from typing import Dict, Any
from datetime import datetime


class AQIService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        self.geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        
    def get_aqi(self, location: str) -> Dict[str, Any]:
        """
        Fetch AQI data for a given location
        
        Args:
            location: City name (e.g., "Pune", "Mumbai, IN")
            
        Returns:
            Normalized AQI data with metadata
        """
        if not self.api_key:
            return self._get_fallback_response(location, "Missing API key")
            
        try:
            # First, get coordinates for the location
            coords = self._get_coordinates(location)
            if not coords:
                return self._get_fallback_response(location, "Location not found")
            
            # Then fetch AQI data
            params = {
                "lat": coords["lat"],
                "lon": coords["lon"],
                "appid": self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return self._normalize_response(data, location)
            
        except requests.exceptions.Timeout:
            return self._get_fallback_response(location, "API timeout")
        except requests.exceptions.RequestException as e:
            return self._get_fallback_response(location, f"API error: {str(e)}")
        except Exception as e:
            return self._get_fallback_response(location, f"Unexpected error: {str(e)}")
    
    def _get_coordinates(self, location: str) -> Dict[str, float]:
        """Get latitude and longitude for a location"""
        try:
            params = {
                "q": location,
                "limit": 1,
                "appid": self.api_key
            }
            response = requests.get(self.geo_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data:
                return {
                    "lat": data[0]["lat"],
                    "lon": data[0]["lon"]
                }
        except:
            pass
        return None
    
    def _normalize_response(self, data: Dict, location: str) -> Dict[str, Any]:
        """Normalize API response to standard format"""
        aqi_data = data.get("list", [{}])[0]
        aqi_value = aqi_data.get("main", {}).get("aqi", 3)
        components = aqi_data.get("components", {})
        
        # AQI levels: 1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor
        aqi_mapping = {
            1: {"level": "Good", "score": 20, "warning": "Air quality is satisfactory"},
            2: {"level": "Fair", "score": 40, "warning": "Air quality is acceptable"},
            3: {"level": "Moderate", "score": 60, "warning": "Sensitive groups may experience issues"},
            4: {"level": "Poor", "score": 80, "warning": "Everyone may experience health effects"},
            5: {"level": "Very Poor", "score": 100, "warning": "Health alert: everyone may experience serious effects"}
        }
        
        aqi_info = aqi_mapping.get(aqi_value, aqi_mapping[3])
        
        return {
            "location": location,
            "aqi_score": aqi_info["score"],
            "aqi_level": aqi_info["level"],
            "pollution_level": aqi_info["level"],
            "health_warning": aqi_info["warning"],
            "pm2_5": components.get("pm2_5"),
            "pm10": components.get("pm10"),
            "o3": components.get("o3"),
            "no2": components.get("no2"),
            "timestamp": datetime.utcnow().isoformat(),
            "source": "OpenWeatherMap Air Pollution API",
            "confidence": "high",
            "status": "success"
        }
    
    def _get_fallback_response(self, location: str, error: str) -> Dict[str, Any]:
        """Return fallback response on error"""
        return {
            "location": location,
            "aqi_score": None,
            "aqi_level": "Unknown",
            "pollution_level": "Unknown",
            "health_warning": "Data unavailable",
            "pm2_5": None,
            "pm10": None,
            "o3": None,
            "no2": None,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "OpenWeatherMap Air Pollution API",
            "confidence": "none",
            "status": "error",
            "error": error
        }
