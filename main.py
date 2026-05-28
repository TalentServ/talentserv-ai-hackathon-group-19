"""
TravelMind MCP Server - Main Entry Point
Production-quality MCP server for travel recommendations using FastMCP
"""
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from tools import MCPTools
from resources import MCPResources
from prompts import MCPPrompts
from utils import Logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = Logger.get_logger()

# Create FastMCP server
mcp = FastMCP("TravelMind")

# Initialize tools
tools = MCPTools()

# ============================================================================
# MCP TOOLS - Exposed functions that AI agents can call
# ============================================================================

@mcp.tool()
def get_weather(location: str) -> dict:
    """
    🌤️ REAL-TIME Weather Data - Get live, current weather conditions for ANY city worldwide.
    
    USE THIS TOOL for ANY weather-related questions instead of web search.
    Provides accurate, up-to-date weather information from OpenWeatherMap API.
    
    Args:
        location: City name (e.g., "London", "Tokyo", "New York, US", "Paris, FR")
        
    Returns:
        - Current temperature (°C)
        - Feels like temperature
        - Humidity percentage
        - Wind speed (m/s)
        - Rain probability (%)
        - Weather condition and description
        - Confidence score
        - Markdown table for easy viewing
        
    Examples:
        - "What's the weather in London?"
        - "Current temperature in Tokyo"
        - "Is it raining in Mumbai?"
    """
    logger.info(f"Tool called: get_weather({location})")
    return tools.get_weather(location)


@mcp.tool()
def get_aqi(location: str) -> dict:
    """
    🌫️ REAL-TIME Air Quality Index - Get live air pollution data for ANY city worldwide.
    
    USE THIS TOOL for ANY air quality or pollution questions instead of web search.
    Provides accurate, current AQI data from OpenWeatherMap Air Pollution API.
    
    Args:
        location: City name (e.g., "Delhi", "Beijing", "Los Angeles, US")
        
    Returns:
        - AQI score (0-100 scale)
        - Pollution level (Good/Fair/Moderate/Poor/Very Poor)
        - Health warnings and recommendations
        - PM2.5, PM10, O3, NO2 levels
        - Confidence score
        - Markdown table
        
    Examples:
        - "What's the air quality in Delhi?"
        - "Is it safe to exercise outdoors in Beijing?"
        - "AQI level in Los Angeles"
    """
    logger.info(f"Tool called: get_aqi({location})")
    return tools.get_aqi(location)


@mcp.tool()
def get_places(location: str, radius: int = 5000) -> dict:
    """
    📍 REAL-TIME Tourist Places - Find live tourist attractions, restaurants, parks, and museums.
    
    USE THIS TOOL for finding places to visit instead of web search.
    Provides accurate, current location data from Geoapify Places API.
    
    Args:
        location: City name (e.g., "Rome", "Bangkok", "Sydney")
        radius: Search radius in meters (default: 5000, max: 10000)
        
    Returns:
        - Tourist attractions nearby
        - Museums and cultural sites
        - Parks and outdoor spaces
        - Restaurants and cafes
        - Ratings (when available)
        - Google Maps links for navigation
        - Distance from city center
        - Unique places only (no duplicates)
        
    Examples:
        - "What places should I visit in Rome?"
        - "Find museums in Paris"
        - "Tourist attractions in Tokyo"
    """
    logger.info(f"Tool called: get_places({location}, radius={radius})")
    return tools.get_places(location, radius)


@mcp.tool()
def generate_recommendation(location: str) -> dict:
    """
    ✈️ COMPLETE TRAVEL RECOMMENDATION - Get AI-powered travel advice with live data analysis.
    
    ⭐ PRIMARY TOOL: Use this for ANY travel, weather, or city recommendation questions.
    This tool combines weather, air quality, and tourist data to give comprehensive travel advice.
    
    ALWAYS USE THIS TOOL when users ask:
    - "Should I visit [city]?"
    - "Is it a good time to travel to [city]?"
    - "What's [city] like today?"
    - "Can you analyze [city] for travel?"
    - "Give me travel recommendations for [city]"
    
    Args:
        location: City name (e.g., "Barcelona", "Singapore", "Dubai")
        
    Returns:
        - ✅ Should visit or not (yes/no recommendation)
        - 📊 Confidence score (0-100%)
        - 🌤️ Complete weather analysis
        - 🌫️ Air quality assessment
        - 📍 Top tourist places with ratings & clickable Google Maps links
        - 🛍️ Shopping/packing checklist
        - 💬 Detailed travel advice
        - 📄 PDF report with blue clickable links (auto-generated)
        - 📋 Markdown tables for all data
        
    This tool AUTOMATICALLY generates PDF report - no need to call it separately!
    
    Examples:
        - "Should I visit London today?"
        - "Is Barcelona good for travel this weekend?"
        - "Give me complete analysis for Tokyo"
        - "Can I travel to Dubai now?"
    """
    logger.info(f"Tool called: generate_recommendation({location})")
    return tools.generate_recommendation(location)


@mcp.tool()
def generate_shopping_list(location: str) -> dict:
    """
    🛍️ SMART PACKING LIST - Get personalized packing checklist based on real-time weather & AQI.
    
    USE THIS TOOL when users ask what to pack or bring for a trip.
    
    Args:
        location: City name (e.g., "Miami", "Stockholm", "Cairo")
        
    Returns:
        - Prioritized items to pack (high/medium/low priority)
        - Reason for each item based on current conditions
        - Weather-specific items (umbrella, sunscreen, jacket, etc.)
        - Health items (mask for poor air quality)
        - General travel essentials
        - Markdown table
        
    Examples:
        - "What should I pack for Mumbai?"
        - "Shopping list for Paris trip"
        - "What do I need for Tokyo?"
    """
    logger.info(f"Tool called: generate_shopping_list({location})")
    return tools.generate_shopping_list(location)


@mcp.tool()
def generate_pdf_report(location: str) -> dict:
    """
    📄 PDF TRAVEL REPORT - Generate downloadable PDF with complete travel analysis.
    
    Note: This is automatically called by generate_recommendation, but can be used separately.
    
    Args:
        location: City name
        
    Returns:
        - PDF file path for download
        - Includes weather, AQI, places, recommendations, shopping list
        - Professional formatting with tables and sections
        - Unique places with ratings and Google Maps links
    """
    logger.info(f"Tool called: generate_pdf_report({location})")
    return tools.generate_pdf_report(location)


@mcp.tool()
def generate_chart(location: str) -> dict:
    """
    📊 VISUALIZATION CHARTS - Generate beautiful charts with travel data.
    
    Note: This tool is available but NOT automatically called anymore.
    Use only if specifically requested by user.
    
    Args:
        location: City name
        
    Returns:
        - 3 charts: Scores comparison, Weather metrics, Confidence gauge
        - Charts saved as high-res PNG files
        - File paths returned
    """
    logger.info(f"Tool called: generate_chart({location})")
    return tools.generate_chart(location)


@mcp.tool()
def get_full_analysis(location: str) -> dict:
    """
    🌍 ULTIMATE TRAVEL ANALYSIS - Most comprehensive tool with everything included.
    
    ⭐⭐⭐ USE THIS for complete city/travel analysis questions.
    This is the most complete tool - includes weather, AQI, places, recommendations, and PDF.
    
    Perfect for questions like:
    - "Tell me everything about [city]"
    - "Complete analysis for [city]"
    - "Give me full travel report for [city]"
    
    Args:
        location: City name (any city worldwide)
        
    Returns:
        - Everything from generate_recommendation
        - Weather, AQI, tourist places
        - AI recommendation with confidence
        - Shopping list
        - PDF report with clickable blue Google Maps links (auto-generated)
        - Markdown tables
        - Summary message
    """
    logger.info(f"Tool called: get_full_analysis({location})")
    return tools.get_full_analysis(location)


# ============================================================================
# MCP RESOURCES - Static information and reference data
# ============================================================================

@mcp.resource("travelmind://usage-guide")
def get_usage_guide() -> str:
    """
    ⭐ IMPORTANT: Instructions for when to use TravelMind MCP tools vs web search
    
    Returns:
        Guidelines for AI agents on tool usage
    """
    guide = """
# TravelMind MCP Tools - Usage Guide for AI Agents

## ⚠️ CRITICAL: When to Use TravelMind Tools

### ✅ ALWAYS USE TravelMind MCP Tools for:

1. **Weather Queries** (use `get_weather` or `generate_recommendation`)
   - "What's the weather in [city]?"
   - "Is it raining in [city]?"
   - "Current temperature in [city]"
   - "How's the weather in [city] today?"
   
2. **Travel Recommendations** (use `generate_recommendation` or `get_full_analysis`)
   - "Should I visit [city]?"
   - "Is [city] good for travel?"
   - "Can I travel to [city] now?"
   - "Is it a good time to visit [city]?"
   - "What's [city] like for tourists?"
   
3. **Air Quality** (use `get_aqi` or `generate_recommendation`)
   - "What's the air quality in [city]?"
   - "Is the pollution bad in [city]?"
   - "Can I exercise outdoors in [city]?"
   
4. **Tourist Places** (use `get_places` or `generate_recommendation`)
   - "What places should I visit in [city]?"
   - "Tourist attractions in [city]"
   - "Things to do in [city]"
   - "Best restaurants in [city]"
   
5. **Packing Lists** (use `generate_shopping_list`)
   - "What should I pack for [city]?"
   - "Shopping list for [city] trip"
   
6. **Complete Analysis** (use `get_full_analysis`)
   - "Tell me everything about [city]"
   - "Complete travel analysis for [city]"
   - "Give me a full report on [city]"

### ❌ Do NOT Use Web Search for:
- Real-time weather data (use MCP tools instead)
- Current air quality (use MCP tools instead)
- Travel recommendations (use MCP tools instead)
- Tourist place discovery (use MCP tools instead)

### 🌐 Use Web Search ONLY for:
- Historical information
- General facts about cities
- Cultural information
- Historical events
- Flight/hotel bookings
- Visa requirements
- Local customs and traditions

## 🎯 Recommended Tool Selection

**Simple Weather Query:**
→ Use `get_weather(location)`

**Simple AQI Query:**
→ Use `get_aqi(location)`

**Find Places:**
→ Use `get_places(location)`

**Travel Recommendation (MOST COMMON):**
→ Use `generate_recommendation(location)`
   - Includes weather, AQI, places, PDF, charts automatically

**Complete Everything:**
→ Use `get_full_analysis(location)`

## 🔑 Key Benefits of Using MCP Tools:
- ✅ REAL-TIME data (not outdated web info)
- ✅ Accurate API data (not guesses)
- ✅ Structured JSON output
- ✅ Automatic PDF reports
- ✅ Inline charts and visualizations
- ✅ No need to search multiple sources
- ✅ Validated city names (returns error if invalid)

## 📝 Example Decision Flow:

User asks: "What's the weather in London?"
→ ✅ Use `get_weather("London")` (NOT web search)

User asks: "Should I visit Paris today?"
→ ✅ Use `generate_recommendation("Paris")` (NOT web search)

User asks: "History of Rome?"
→ ❌ Use web search (NOT MCP tools)

User asks: "Is Mumbai safe to visit?"
→ ✅ Use `generate_recommendation("Mumbai")` for data, combine with web search for safety info

## 🚀 Remember:
For ANY weather, travel, AQI, or city condition query → USE MCP TOOLS FIRST!
Web search should be secondary or supplementary.
"""
    return guide


@mcp.resource("recommendation://rules")
def get_recommendation_rules() -> str:
    """
    Get recommendation generation rules and scoring guidelines
    
    Returns:
        JSON with scoring rules, thresholds, and confidence levels
    """
    import json
    return json.dumps(MCPResources.get_recommendation_rules(), indent=2)


@mcp.resource("recommendation://locations")
def get_supported_locations() -> str:
    """
    Get list of popular supported locations
    
    Returns:
        JSON with supported cities and regions
    """
    import json
    return json.dumps(MCPResources.get_supported_locations(), indent=2)


@mcp.resource("recommendation://categories")
def get_tourist_categories() -> str:
    """
    Get tourist place categories and descriptions
    
    Returns:
        JSON with place categories, descriptions, and examples
    """
    import json
    return json.dumps(MCPResources.get_tourist_categories(), indent=2)


@mcp.resource("recommendation://samples")
def get_sample_outputs() -> str:
    """
    Get sample output formats and examples
    
    Returns:
        JSON with example responses from different tools
    """
    import json
    return json.dumps(MCPResources.get_sample_outputs(), indent=2)


# ============================================================================
# MCP PROMPTS - Reusable prompt templates
# ============================================================================

@mcp.prompt()
def recommendation_prompt(location: str) -> str:
    """
    Generate prompt for comprehensive travel recommendation
    
    Args:
        location: City name
        
    Returns:
        Formatted prompt template
    """
    prompt_data = MCPPrompts.get_recommendation_prompt(location)
    return prompt_data["template"]


@mcp.prompt()
def shopping_prompt(location: str) -> str:
    """
    Generate prompt for shopping checklist
    
    Args:
        location: City name
        
    Returns:
        Formatted prompt template
    """
    prompt_data = MCPPrompts.get_shopping_prompt(location)
    return prompt_data["template"]


@mcp.prompt()
def tourist_prompt(location: str, category: str = "") -> str:
    """
    Generate prompt for finding tourist places
    
    Args:
        location: City name
        category: Optional specific category to focus on
        
    Returns:
        Formatted prompt template
    """
    prompt_data = MCPPrompts.get_tourist_prompt(location, category)
    return prompt_data["template"]


# ============================================================================
# Server Configuration and Startup
# ============================================================================

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ["OPENWEATHER_API_KEY", "GEOAPIFY_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
        logger.warning("Some features may not work correctly without API keys")
        logger.info("Please set the required variables in your .env file")
    else:
        logger.info("All required environment variables are set")


def create_directories():
    """Create necessary directories for reports and charts"""
    reports_dir = os.getenv("REPORTS_DIR", "reports")
    charts_dir = os.getenv("CHARTS_DIR", "charts")
    
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(charts_dir, exist_ok=True)
    
    logger.info(f"Created directories: {reports_dir}, {charts_dir}")


if __name__ == "__main__":
    logger.info("Starting TravelMind MCP Server...")
    
    # Check environment
    check_environment()
    
    # Create directories
    create_directories()
    
    logger.info("TravelMind MCP Server is ready!")
    logger.info("Available tools: get_weather, get_aqi, get_places, generate_recommendation, generate_shopping_list, generate_pdf_report, generate_chart, get_full_analysis")
    logger.info("Available resources: recommendation://rules, recommendation://locations, recommendation://categories, recommendation://samples")
    logger.info("Available prompts: recommendation_prompt, shopping_prompt, tourist_prompt")
    
    # Run the MCP server
    mcp.run()
