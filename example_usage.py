# Example Usage Script
"""
This script demonstrates how to use the TravelMind services directly
without going through the MCP protocol layer.
Useful for testing and debugging.
"""
import os
from dotenv import load_dotenv
from services import WeatherService, AQIService, PlacesService, RecommendationService
from services.pdf_service import PDFService
from services.chart_service import ChartService
from utils import MarkdownTableGenerator

# Load environment variables
load_dotenv()


def main():
    """Run example queries"""
    location = "Pune"
    
    print("=" * 60)
    print(f"TravelMind Example - Analyzing {location}")
    print("=" * 60)
    
    # Initialize services
    weather_service = WeatherService()
    aqi_service = AQIService()
    places_service = PlacesService()
    recommendation_service = RecommendationService()
    pdf_service = PDFService()
    chart_service = ChartService()
    
    # 1. Get Weather
    print("\n1. Fetching Weather Data...")
    weather_data = weather_service.get_weather(location)
    print(f"   Temperature: {weather_data.get('temperature')}°C")
    print(f"   Rain Probability: {weather_data.get('rain_probability')}%")
    print(f"   Status: {weather_data.get('status')}")
    
    # 2. Get AQI
    print("\n2. Fetching AQI Data...")
    aqi_data = aqi_service.get_aqi(location)
    print(f"   AQI Score: {aqi_data.get('aqi_score')}")
    print(f"   Pollution Level: {aqi_data.get('pollution_level')}")
    print(f"   Status: {aqi_data.get('status')}")
    
    # 3. Get Places
    print("\n3. Fetching Tourist Places...")
    places_data = places_service.get_places(location)
    print(f"   Total Places: {places_data.get('total_places')}")
    print(f"   Status: {places_data.get('status')}")
    
    # 4. Generate Recommendation
    print("\n4. Generating Recommendation...")
    recommendation = recommendation_service.generate_recommendation(
        weather_data, aqi_data, places_data
    )
    print(f"   Should Visit: {recommendation.get('should_visit')}")
    print(f"   Confidence: {recommendation.get('confidence_score')}%")
    print(f"   Recommendation: {recommendation.get('recommendation')}")
    
    # 5. Generate Shopping List
    print("\n5. Generating Shopping List...")
    shopping_list = recommendation_service.generate_shopping_list(
        weather_data, aqi_data
    )
    print(f"   Total Items: {shopping_list.get('total_items')}")
    for item in shopping_list.get('items', [])[:3]:
        print(f"   - {item.get('item')}: {item.get('reason')}")
    
    # 6. Generate Markdown Tables
    print("\n6. Generating Markdown Tables...")
    weather_table = MarkdownTableGenerator.generate_weather_table(weather_data)
    print("\n   Weather Table:")
    print(weather_table)
    
    # 7. Generate PDF Report
    print("\n7. Generating PDF Report...")
    pdf_result = pdf_service.generate_pdf_report(
        weather_data, aqi_data, places_data, recommendation, shopping_list
    )
    if pdf_result.get('status') == 'success':
        print(f"   PDF Generated: {pdf_result.get('file_path')}")
    else:
        print(f"   PDF Error: {pdf_result.get('error')}")
    
    # 8. Generate Charts
    print("\n8. Generating Charts...")
    chart_result = chart_service.generate_chart(
        weather_data, aqi_data, recommendation
    )
    if chart_result.get('status') == 'success':
        print(f"   Charts Generated:")
        for chart_name, chart_path in chart_result.get('charts', {}).items():
            print(f"   - {chart_name}: {chart_path}")
    else:
        print(f"   Chart Error: {chart_result.get('error')}")
    
    print("\n" + "=" * 60)
    print("Example Complete!")
    print("=" * 60)


if __name__ == "__main__":
    # Check if API keys are set
    if not os.getenv("OPENWEATHER_API_KEY"):
        print("ERROR: OPENWEATHER_API_KEY not set in .env file")
        exit(1)
    
    if not os.getenv("GEOAPIFY_API_KEY"):
        print("ERROR: GEOAPIFY_API_KEY not set in .env file")
        exit(1)
    
    main()
