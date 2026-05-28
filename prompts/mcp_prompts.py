"""
MCP Prompts - Reusable prompt templates for AI agents
"""
from typing import Dict, Any


class MCPPrompts:
    
    @staticmethod
    def get_recommendation_prompt(location: str = "{location}") -> Dict[str, Any]:
        """Get prompt template for generating recommendations"""
        return {
            "name": "recommendation_prompt",
            "description": "Generate comprehensive travel recommendation",
            "template": f"""
You are a travel advisor AI. Analyze the following data and provide a comprehensive travel recommendation for {location}.

Consider:
1. Current weather conditions (temperature, rain probability, wind)
2. Air quality index and health implications
3. Available tourist attractions and activities
4. Overall safety and comfort factors

Provide:
- Clear recommendation (should visit or not)
- Confidence level with explanation
- Practical travel advice
- Top attractions to visit
- Shopping checklist for the trip

Be specific, practical, and consider the user's safety and comfort.
""",
            "parameters": {
                "location": {
                    "type": "string",
                    "description": "City or location name",
                    "required": True
                }
            },
            "example_usage": "Generate a recommendation for visiting Pune this evening",
            "expected_tools": [
                "get_weather",
                "get_aqi",
                "get_places",
                "generate_recommendation",
                "generate_shopping_list"
            ]
        }
    
    @staticmethod
    def get_shopping_prompt(location: str = "{location}") -> Dict[str, Any]:
        """Get prompt template for generating shopping lists"""
        return {
            "name": "shopping_prompt",
            "description": "Generate shopping checklist for travel",
            "template": f"""
You are a travel packing assistant. Based on current weather and air quality conditions in {location}, create a practical shopping checklist.

Consider:
1. Temperature (hot/cold weather items)
2. Rain probability (rain protection)
3. Air quality (masks, health items)
4. General travel essentials

Provide a prioritized list with:
- Item name
- Reason for including it
- Priority level (high/medium/low)

Be practical and focus on items that will genuinely improve the travel experience.
""",
            "parameters": {
                "location": {
                    "type": "string",
                    "description": "City or location name",
                    "required": True
                }
            },
            "example_usage": "What should I pack for a trip to Mumbai?",
            "expected_tools": [
                "get_weather",
                "get_aqi",
                "generate_shopping_list"
            ]
        }
    
    @staticmethod
    def get_tourist_prompt(location: str = "{location}", category: str = "{category}") -> Dict[str, Any]:
        """Get prompt template for finding tourist places"""
        return {
            "name": "tourist_prompt",
            "description": "Find and recommend tourist attractions",
            "template": f"""
You are a local tour guide AI. Help users discover interesting places to visit in {location}.

Focus on:
1. Tourist attractions and landmarks
2. Museums and cultural sites
3. Parks and outdoor spaces
4. Dining and entertainment options

{f'Specifically focus on: {category}' if category != "{category}" else ''}

Provide:
- List of places sorted by distance
- Brief description of each place
- Category and type
- Practical visit information

Make recommendations based on proximity and popularity.
""",
            "parameters": {
                "location": {
                    "type": "string",
                    "description": "City or location name",
                    "required": True
                },
                "category": {
                    "type": "string",
                    "description": "Specific category to focus on (optional)",
                    "required": False
                }
            },
            "example_usage": "What are the best museums to visit in Delhi?",
            "expected_tools": [
                "get_places"
            ]
        }
    
    @staticmethod
    def get_weather_analysis_prompt(location: str = "{location}") -> Dict[str, Any]:
        """Get prompt template for weather analysis"""
        return {
            "name": "weather_analysis_prompt",
            "description": "Analyze weather conditions for outdoor activities",
            "template": f"""
You are a weather analysis AI. Evaluate current weather conditions in {location} for outdoor activities.

Analyze:
1. Temperature and feels-like temperature
2. Humidity levels
3. Wind speed and conditions
4. Precipitation probability
5. Overall comfort level

Provide:
- Weather suitability score (0-100)
- Best and worst aspects of current weather
- Recommendations for outdoor vs indoor activities
- Time of day recommendations
- What to wear/bring

Be specific about how weather impacts different types of activities.
""",
            "parameters": {
                "location": {
                    "type": "string",
                    "description": "City or location name",
                    "required": True
                }
            },
            "example_usage": "Is the weather good for sightseeing in Goa today?",
            "expected_tools": [
                "get_weather"
            ]
        }
    
    @staticmethod
    def get_air_quality_prompt(location: str = "{location}") -> Dict[str, Any]:
        """Get prompt template for air quality analysis"""
        return {
            "name": "air_quality_prompt",
            "description": "Analyze air quality and health implications",
            "template": f"""
You are an environmental health AI. Assess air quality conditions in {location} and provide health guidance.

Analyze:
1. Current AQI score and pollution level
2. Specific pollutants (PM2.5, PM10, O3, NO2)
3. Health implications for different groups
4. Activity recommendations

Provide:
- Air quality assessment
- Health warnings and precautions
- Recommended protective measures
- Suitable vs unsuitable activities
- Vulnerable group considerations (children, elderly, respiratory issues)

Be clear about health risks and practical protective measures.
""",
            "parameters": {
                "location": {
                    "type": "string",
                    "description": "City or location name",
                    "required": True
                }
            },
            "example_usage": "Is it safe to exercise outdoors in Delhi today?",
            "expected_tools": [
                "get_aqi"
            ]
        }
    
    @staticmethod
    def get_complete_analysis_prompt(location: str = "{location}") -> Dict[str, Any]:
        """Get prompt template for complete travel analysis"""
        return {
            "name": "complete_analysis_prompt",
            "description": "Generate comprehensive travel analysis with all data",
            "template": f"""
You are a comprehensive travel planning AI. Provide a complete analysis for visiting {location}.

Generate:
1. Weather analysis and forecast implications
2. Air quality assessment and health guidance
3. Top tourist attractions and activities
4. Overall travel recommendation with confidence score
5. Practical advice and safety considerations
6. Shopping/packing checklist
7. Visual reports (PDF and charts)

Deliver:
- Structured recommendation with clear yes/no advice
- Confidence level with detailed explanation
- Markdown tables for easy reading
- PDF report for offline reference
- Charts for visual understanding
- Actionable next steps

Provide a complete package that helps users make an informed decision.
""",
            "parameters": {
                "location": {
                    "type": "string",
                    "description": "City or location name",
                    "required": True
                }
            },
            "example_usage": "Should I visit Bangalore this weekend? Give me a complete analysis.",
            "expected_tools": [
                "get_weather",
                "get_aqi",
                "get_places",
                "generate_recommendation",
                "generate_shopping_list",
                "generate_pdf_report",
                "generate_chart"
            ]
        }
    
    @staticmethod
    def get_all_prompts() -> Dict[str, Any]:
        """Get all available prompts"""
        return {
            "recommendation": MCPPrompts.get_recommendation_prompt(),
            "shopping": MCPPrompts.get_shopping_prompt(),
            "tourist": MCPPrompts.get_tourist_prompt(),
            "weather_analysis": MCPPrompts.get_weather_analysis_prompt(),
            "air_quality": MCPPrompts.get_air_quality_prompt(),
            "complete_analysis": MCPPrompts.get_complete_analysis_prompt()
        }
