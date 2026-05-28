"""
Places service for fetching tourist attractions and points of interest using Geoapify API
"""
import os
import requests
from typing import Dict, Any, List
from datetime import datetime


class PlacesService:
    def __init__(self):
        self.api_key = os.getenv("GEOAPIFY_API_KEY")
        self.base_url = "https://api.geoapify.com/v2/places"
        self.geocoding_url = "https://api.geoapify.com/v1/geocode/search"
        
    def get_places(self, location: str, radius: int = 5000) -> Dict[str, Any]:
        """
        Fetch tourist places and attractions for a given location
        
        Args:
            location: City name (e.g., "Pune", "Mumbai")
            radius: Search radius in meters (default: 5000)
            
        Returns:
            Normalized places data with metadata
        """
        if not self.api_key:
            return self._get_fallback_response(location, "Missing API key")
            
        try:
            # First, get coordinates for the location
            coords = self._get_coordinates(location)
            if not coords:
                return self._get_fallback_response(location, "Location not found")
            
            # Fetch different categories of places
            categories = [
                "tourism.attraction",
                "entertainment.museum",
                "leisure.park",
                "catering.restaurant"
            ]
            
            all_places = []
            for category in categories:
                places = self._fetch_places_by_category(coords, category, radius)
                all_places.extend(places)
            
            return self._normalize_response(all_places, location)
            
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
                "text": location,
                "limit": 1,
                "apiKey": self.api_key
            }
            response = requests.get(self.geocoding_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("features"):
                coords = data["features"][0]["geometry"]["coordinates"]
                return {
                    "lat": coords[1],
                    "lon": coords[0]
                }
        except:
            pass
        return None
    
    def _fetch_places_by_category(self, coords: Dict, category: str, radius: int) -> List[Dict]:
        """Fetch places for a specific category"""
        try:
            params = {
                "categories": category,
                "filter": f"circle:{coords['lon']},{coords['lat']},{radius}",
                "limit": 20,
                "apiKey": self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            places = []
            for feature in data.get("features", []):
                props = feature.get("properties", {})
                geometry = feature.get("geometry", {}).get("coordinates", [])
                
                # Get coordinates for Google Maps link
                place_lon = geometry[0] if len(geometry) > 0 else None
                place_lat = geometry[1] if len(geometry) > 1 else None
                
                place_data = {
                    "name": props.get("name", "Unknown"),
                    "category": self._format_category(category),
                    "address": props.get("address_line2", "Address not available"),
                    "distance": props.get("distance", 0),
                    "rating": props.get("datasource", {}).get("raw", {}).get("rating", None),
                    "google_maps_link": f"https://www.google.com/maps/search/?api=1&query={place_lat},{place_lon}" if place_lat and place_lon else None,
                    "lat": place_lat,
                    "lon": place_lon
                }
                places.append(place_data)
            
            return places
        except:
            return []
    
    def _format_category(self, category: str) -> str:
        """Format category string for display"""
        mapping = {
            "tourism.attraction": "Tourist Attraction",
            "entertainment.museum": "Museum",
            "leisure.park": "Park",
            "catering.restaurant": "Restaurant"
        }
        return mapping.get(category, category)
    
    def _normalize_response(self, places: List[Dict], location: str) -> Dict[str, Any]:
        """Normalize API response to standard format"""
        # Remove duplicates by name (keep the closest one)
        seen = {}
        unique_places = []
        for place in places:
            name = place["name"]
            if name not in seen:
                seen[name] = place
                unique_places.append(place)
            else:
                # Keep the closer one
                if place["distance"] < seen[name]["distance"]:
                    unique_places.remove(seen[name])
                    seen[name] = place
                    unique_places.append(place)
        
        # Sort by distance
        unique_places.sort(key=lambda x: x["distance"])
        unique_places = unique_places[:20]
        
        # Group by category
        grouped = {
            "tourist_attractions": [p for p in unique_places if p["category"] == "Tourist Attraction"],
            "museums": [p for p in unique_places if p["category"] == "Museum"],
            "parks": [p for p in unique_places if p["category"] == "Park"],
            "restaurants": [p for p in unique_places if p["category"] == "Restaurant"]
        }
        
        return {
            "location": location,
            "total_places": len(unique_places),
            "places": unique_places,
            "grouped_places": grouped,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "Geoapify Places API",
            "confidence": "high" if len(unique_places) > 0 else "low",
            "status": "success"
        }
    
    def _get_fallback_response(self, location: str, error: str) -> Dict[str, Any]:
        """Return fallback response on error"""
        return {
            "location": location,
            "total_places": 0,
            "places": [],
            "grouped_places": {
                "tourist_attractions": [],
                "museums": [],
                "parks": [],
                "restaurants": []
            },
            "timestamp": datetime.utcnow().isoformat(),
            "source": "Geoapify Places API",
            "confidence": "none",
            "status": "error",
            "error": error
        }
