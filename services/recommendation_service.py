"""
Recommendation service for generating intelligent travel recommendations
"""
from typing import Dict, Any, List
from datetime import datetime


class RecommendationService:
    
    def generate_recommendation(self, weather_data: Dict, aqi_data: Dict, places_data: Dict) -> Dict[str, Any]:
        """
        Generate intelligent travel recommendation based on aggregated data
        
        Args:
            weather_data: Weather information
            aqi_data: Air quality information
            places_data: Tourist places information
            
        Returns:
            Comprehensive recommendation with confidence score
        """
        location = weather_data.get("location", "Unknown")
        
        # Calculate individual scores
        weather_score = self._calculate_weather_score(weather_data)
        aqi_score = self._calculate_aqi_score(aqi_data)
        places_score = self._calculate_places_score(places_data)
        
        # Calculate overall confidence
        overall_confidence = (weather_score + aqi_score + places_score) / 3
        
        # Generate recommendation
        recommendation = self._generate_recommendation_text(
            weather_data, aqi_data, places_data, overall_confidence
        )
        
        # Generate travel advice
        advice = self._generate_travel_advice(weather_data, aqi_data, overall_confidence)
        
        # Get top places to visit
        top_places = self._get_top_places(places_data)
        
        return {
            "location": location,
            "recommendation": recommendation,
            "should_visit": overall_confidence >= 60,
            "confidence_score": round(overall_confidence, 1),
            "confidence_level": self._get_confidence_level(overall_confidence),
            "travel_advice": advice,
            "top_places": top_places,
            "weather_score": round(weather_score, 1),
            "aqi_score": round(aqi_score, 1),
            "places_score": round(places_score, 1),
            "explanation": self._generate_explanation(weather_data, aqi_data, places_data, overall_confidence),
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success"
        }
    
    def _calculate_weather_score(self, weather_data: Dict) -> float:
        """Calculate score based on weather conditions (0-100)"""
        if weather_data.get("status") == "error":
            return 50  # Neutral score on error
        
        score = 100
        
        temp = weather_data.get("temperature")
        if temp:
            # Ideal temperature: 20-28°C
            if temp < 15:
                score -= 30
            elif temp < 20:
                score -= 15
            elif temp > 35:
                score -= 30
            elif temp > 30:
                score -= 15
        
        rain_prob = weather_data.get("rain_probability", 0)
        if rain_prob > 70:
            score -= 30
        elif rain_prob > 40:
            score -= 15
        
        wind_speed = weather_data.get("wind_speed", 0)
        if wind_speed > 20:
            score -= 20
        elif wind_speed > 15:
            score -= 10
        
        return max(0, score)
    
    def _calculate_aqi_score(self, aqi_data: Dict) -> float:
        """Calculate score based on air quality (0-100)"""
        if aqi_data.get("status") == "error":
            return 50  # Neutral score on error
        
        aqi_value = aqi_data.get("aqi_score")
        if aqi_value is None:
            return 50
        
        # Invert AQI score (lower AQI = better air quality)
        # AQI: 0-20=Good, 21-40=Fair, 41-60=Moderate, 61-80=Poor, 81-100=Very Poor
        if aqi_value <= 20:
            return 100
        elif aqi_value <= 40:
            return 80
        elif aqi_value <= 60:
            return 60
        elif aqi_value <= 80:
            return 40
        else:
            return 20
    
    def _calculate_places_score(self, places_data: Dict) -> float:
        """Calculate score based on available places (0-100)"""
        if places_data.get("status") == "error":
            return 50  # Neutral score on error
        
        total_places = places_data.get("total_places", 0)
        
        if total_places >= 15:
            return 100
        elif total_places >= 10:
            return 80
        elif total_places >= 5:
            return 60
        elif total_places >= 2:
            return 40
        else:
            return 20
    
    def _generate_recommendation_text(self, weather_data: Dict, aqi_data: Dict, 
                                     places_data: Dict, confidence: float) -> str:
        """Generate human-readable recommendation"""
        location = weather_data.get("location", "this location")
        
        if confidence >= 80:
            return f"Excellent time to visit {location}! Conditions are ideal for outdoor activities."
        elif confidence >= 60:
            return f"Good time to visit {location}. Weather and air quality are favorable."
        elif confidence >= 40:
            return f"Moderate conditions in {location}. Consider indoor activities or plan accordingly."
        else:
            return f"Not the best time to visit {location}. Consider postponing or staying indoors."
    
    def _generate_travel_advice(self, weather_data: Dict, aqi_data: Dict, confidence: float) -> List[str]:
        """Generate practical travel advice"""
        advice = []
        
        temp = weather_data.get("temperature")
        if temp and temp > 30:
            advice.append("Stay hydrated and wear light clothing")
        elif temp and temp < 15:
            advice.append("Bring warm clothing")
        
        rain_prob = weather_data.get("rain_probability", 0)
        if rain_prob > 40:
            advice.append("Carry an umbrella or raincoat")
        
        aqi_level = aqi_data.get("aqi_level", "")
        if aqi_level in ["Poor", "Very Poor"]:
            advice.append("Wear a mask due to poor air quality")
        
        if confidence < 60:
            advice.append("Consider indoor attractions")
        
        return advice if advice else ["Enjoy your visit!"]
    
    def _get_top_places(self, places_data: Dict, limit: int = 5) -> List[Dict]:
        """Get top places to visit"""
        places = places_data.get("places", [])
        return places[:limit]
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Convert confidence score to level"""
        if confidence >= 80:
            return "Very High"
        elif confidence >= 60:
            return "High"
        elif confidence >= 40:
            return "Moderate"
        else:
            return "Low"
    
    def _generate_explanation(self, weather_data: Dict, aqi_data: Dict, 
                            places_data: Dict, confidence: float) -> str:
        """Generate detailed explanation of the recommendation"""
        parts = []
        
        if weather_data.get("status") == "success":
            temp = weather_data.get("temperature")
            rain = weather_data.get("rain_probability")
            parts.append(f"Weather: {temp}°C, {rain}% rain probability")
        
        if aqi_data.get("status") == "success":
            aqi_level = aqi_data.get("aqi_level")
            parts.append(f"Air Quality: {aqi_level}")
        
        if places_data.get("status") == "success":
            total = places_data.get("total_places")
            parts.append(f"{total} attractions nearby")
        
        explanation = ". ".join(parts) + "."
        explanation += f" Overall confidence: {self._get_confidence_level(confidence)}."
        
        return explanation
    
    def generate_shopping_list(self, weather_data: Dict, aqi_data: Dict) -> Dict[str, Any]:
        """
        Generate shopping checklist based on weather and AQI
        
        Args:
            weather_data: Weather information
            aqi_data: Air quality information
            
        Returns:
            Shopping list with items and reasons
        """
        items = []
        
        # Weather-based items
        temp = weather_data.get("temperature")
        rain_prob = weather_data.get("rain_probability", 0)
        
        if rain_prob > 40:
            items.append({
                "item": "Umbrella",
                "reason": f"{rain_prob}% chance of rain",
                "priority": "high" if rain_prob > 70 else "medium"
            })
        
        if temp and temp > 28:
            items.append({
                "item": "Sunscreen",
                "reason": f"High temperature ({temp}°C)",
                "priority": "high"
            })
            items.append({
                "item": "Water Bottle",
                "reason": "Stay hydrated in warm weather",
                "priority": "high"
            })
            items.append({
                "item": "Sunglasses",
                "reason": "Protect from sun",
                "priority": "medium"
            })
        
        if temp and temp < 18:
            items.append({
                "item": "Jacket",
                "reason": f"Cool temperature ({temp}°C)",
                "priority": "high"
            })
        
        # AQI-based items
        aqi_level = aqi_data.get("aqi_level", "")
        if aqi_level in ["Poor", "Very Poor", "Moderate"]:
            items.append({
                "item": "Face Mask",
                "reason": f"Air quality is {aqi_level}",
                "priority": "high" if aqi_level in ["Poor", "Very Poor"] else "medium"
            })
        
        # Always useful items
        items.append({
            "item": "Phone Charger",
            "reason": "Essential for navigation and communication",
            "priority": "medium"
        })
        
        return {
            "location": weather_data.get("location", "Unknown"),
            "items": items,
            "total_items": len(items),
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success"
        }
