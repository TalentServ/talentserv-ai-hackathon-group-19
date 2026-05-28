"""
MCP Tools implementation
"""
import os
from typing import Dict, Any
from datetime import datetime
from services import WeatherService, AQIService, PlacesService, RecommendationService
from services.pdf_service import PDFService
from services.chart_service import ChartService
from utils import MarkdownTableGenerator, Logger


class MCPTools:
    def __init__(self):
        self.weather_service = WeatherService()
        self.aqi_service = AQIService()
        self.places_service = PlacesService()
        self.recommendation_service = RecommendationService()
        self.pdf_service = PDFService()
        self.chart_service = ChartService()
        self.logger = Logger.get_logger()
    
    def get_weather(self, location: str) -> Dict[str, Any]:
        """
        Get weather data for a location
        
        Args:
            location: City name (e.g., "Pune", "Mumbai, IN")
            
        Returns:
            Weather data with metadata
        """
        self.logger.info(f"Fetching weather for: {location}")
        result = self.weather_service.get_weather(location)
        
        # Add markdown table
        result["markdown_table"] = MarkdownTableGenerator.generate_weather_table(result)
        
        return result
    
    def get_aqi(self, location: str) -> Dict[str, Any]:
        """
        Get air quality index for a location
        
        Args:
            location: City name (e.g., "Pune", "Mumbai, IN")
            
        Returns:
            AQI data with metadata
        """
        self.logger.info(f"Fetching AQI for: {location}")
        result = self.aqi_service.get_aqi(location)
        
        # Add markdown table
        result["markdown_table"] = MarkdownTableGenerator.generate_aqi_table(result)
        
        return result
    
    def get_places(self, location: str, radius: int = 5000) -> Dict[str, Any]:
        """
        Get tourist places and attractions for a location
        
        Args:
            location: City name (e.g., "Pune", "Mumbai")
            radius: Search radius in meters (default: 5000)
            
        Returns:
            Places data with metadata
        """
        self.logger.info(f"Fetching places for: {location}")
        result = self.places_service.get_places(location, radius)
        
        # Add markdown table
        result["markdown_table"] = MarkdownTableGenerator.generate_places_table(
            result.get("places", [])
        )
        
        return result
    
    def generate_recommendation(self, location: str) -> Dict[str, Any]:
        """
        Generate comprehensive travel recommendation with PDF (no charts)
        
        Args:
            location: City name (e.g., "Pune", "Mumbai")
            
        Returns:
            Comprehensive recommendation with all data and PDF
        """
        self.logger.info(f"Generating recommendation for: {location}")
        
        # Fetch all data
        weather_data = self.weather_service.get_weather(location)
        
        # Check if city was found
        if weather_data.get("status") == "error" and "not found" in weather_data.get("error", "").lower():
            return {
                "status": "error",
                "location": location,
                "error": weather_data.get("error"),
                "message": f"❌ City '{location}' not found. Please enter a correct city name.",
                "recommendation": "Unable to generate recommendation for invalid city.",
                "should_visit": False,
                "confidence_score": 0,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        aqi_data = self.aqi_service.get_aqi(location)
        places_data = self.places_service.get_places(location)
        
        # Generate recommendation
        recommendation = self.recommendation_service.generate_recommendation(
            weather_data, aqi_data, places_data
        )
        
        # Generate shopping list
        shopping_list = self.recommendation_service.generate_shopping_list(
            weather_data, aqi_data
        )
        
        # Generate PDF report
        pdf_result = self.pdf_service.generate_pdf_report(
            weather_data, aqi_data, places_data, recommendation, shopping_list
        )
        
        # Add comparison table
        recommendation["comparison_table"] = MarkdownTableGenerator.generate_comparison_table(
            weather_data, aqi_data, recommendation
        )
        
        # Include all data
        recommendation["source_data"] = {
            "weather": weather_data,
            "aqi": aqi_data,
            "places": places_data
        }
        
        recommendation["shopping_list"] = shopping_list
        recommendation["pdf_report"] = pdf_result
        
        # Add full PDF path
        if pdf_result.get("status") == "success":
            full_path = os.path.abspath(pdf_result.get("file_path", ""))
            recommendation["pdf_report"]["full_path"] = full_path
        
        return recommendation
    
    def generate_shopping_list(self, location: str) -> Dict[str, Any]:
        """
        Generate shopping checklist based on weather and AQI
        
        Args:
            location: City name (e.g., "Pune", "Mumbai")
            
        Returns:
            Shopping checklist with items and reasons
        """
        self.logger.info(f"Generating shopping list for: {location}")
        
        # Fetch weather and AQI
        weather_data = self.weather_service.get_weather(location)
        aqi_data = self.aqi_service.get_aqi(location)
        
        # Generate shopping list
        shopping_list = self.recommendation_service.generate_shopping_list(
            weather_data, aqi_data
        )
        
        # Add markdown table
        shopping_list["markdown_table"] = MarkdownTableGenerator.generate_shopping_table(
            shopping_list
        )
        
        return shopping_list
    
    def generate_pdf_report(self, location: str) -> Dict[str, Any]:
        """
        Generate comprehensive PDF report
        
        Args:
            location: City name (e.g., "Pune", "Mumbai")
            
        Returns:
            PDF report metadata with file path
        """
        self.logger.info(f"Generating PDF report for: {location}")
        
        # Fetch all data
        weather_data = self.weather_service.get_weather(location)
        aqi_data = self.aqi_service.get_aqi(location)
        places_data = self.places_service.get_places(location)
        
        # Generate recommendation and shopping list
        recommendation = self.recommendation_service.generate_recommendation(
            weather_data, aqi_data, places_data
        )
        shopping_list = self.recommendation_service.generate_shopping_list(
            weather_data, aqi_data
        )
        
        # Generate PDF
        result = self.pdf_service.generate_pdf_report(
            weather_data, aqi_data, places_data, recommendation, shopping_list
        )
        
        return result
    
    def generate_chart(self, location: str) -> Dict[str, Any]:
        """
        Generate visualization charts
        
        Args:
            location: City name (e.g., "Pune", "Mumbai")
            
        Returns:
            Chart metadata with file paths
        """
        self.logger.info(f"Generating charts for: {location}")
        
        # Fetch all data
        weather_data = self.weather_service.get_weather(location)
        aqi_data = self.aqi_service.get_aqi(location)
        places_data = self.places_service.get_places(location)
        
        # Generate recommendation
        recommendation = self.recommendation_service.generate_recommendation(
            weather_data, aqi_data, places_data
        )
        
        # Generate charts
        result = self.chart_service.generate_chart(
            weather_data, aqi_data, recommendation
        )
        
        return result
    
    def get_full_analysis(self, location: str) -> Dict[str, Any]:
        """
        Get complete analysis with all data, recommendations, and PDF
        
        Args:
            location: City name (e.g., "Pune", "Mumbai")
            
        Returns:
            Complete analysis package
        """
        self.logger.info(f"Generating full analysis for: {location}")
        
        # Get comprehensive recommendation (includes PDF)
        recommendation = self.generate_recommendation(location)
        
        # Check if city was found
        if recommendation.get("status") == "error":
            return recommendation
        
        return {
            "location": location,
            "analysis": recommendation,
            "status": "success",
            "message": f"✅ Complete analysis for {location} generated successfully!",
            "includes": [
                "Weather data",
                "Air quality index",
                "Tourist places with Google Maps links",
                "Travel recommendation",
                "Shopping checklist",
                "PDF report"
            ]
        }
