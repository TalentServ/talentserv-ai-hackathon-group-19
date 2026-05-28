# TravelMind MCP Server

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-0.1.0-green.svg)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**TravelMind** is a production-quality MCP (Model Context Protocol) server that provides intelligent travel recommendations by aggregating data from multiple external APIs. Built with Python, FastAPI, and FastMCP, it enables AI agents like Cursor, Claude Desktop, and OpenAI Agents to fetch weather data, air quality indexes, tourist places, and generate comprehensive travel recommendations.

## 🎯 Features

- **Multi-Source Data Aggregation**: Combines weather, AQI, and places data
- **Intelligent Recommendations**: AI-powered travel advice with confidence scoring
- **MCP Tools**: 8 exposed tools for AI agents to interact with
- **MCP Resources**: Static reference data and guidelines
- **MCP Prompts**: Reusable prompt templates
- **Structured JSON Output**: Normalized responses with metadata
- **Markdown Tables**: Formatted tables for easy reading
- **PDF Reports**: Comprehensive downloadable reports
- **Data Visualization**: Charts for scores and metrics
- **Error Handling**: Graceful fallbacks and retry logic
- **Production-Ready**: Modular, tested, and well-documented

## 📋 Table of Contents

- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [MCP Tools](#mcp-tools)
- [MCP Resources](#mcp-resources)
- [MCP Prompts](#mcp-prompts)
- [API Integration](#api-integration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Example Flow](#example-flow)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent (Cursor/Claude)                  │
└───────────────────────────┬─────────────────────────────────┘
                            │ MCP Protocol
┌───────────────────────────▼─────────────────────────────────┐
│                   TravelMind MCP Server                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  MCP Tools  │  │  Resources  │  │   Prompts   │        │
│  └──────┬──────┘  └─────────────┘  └─────────────┘        │
│         │                                                    │
│  ┌──────▼──────────────────────────────────────────────┐   │
│  │           Recommendation Engine                     │   │
│  └──────┬──────────────────────────────────────────────┘   │
│         │                                                    │
│  ┌──────▼────────┐  ┌──────────┐  ┌──────────┐            │
│  │   Services    │  │ Utilities│  │PDF/Charts│            │
│  └──────┬────────┘  └──────────┘  └──────────┘            │
└─────────┼────────────────────────────────────────────────────┘
          │
    ┌─────▼─────┐
    │ External  │
    │   APIs    │
    │           │
    │ • Weather │
    │ • AQI     │
    │ • Places  │
    └───────────┘
```

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager
- API keys for external services

### Steps

1. **Clone or download the project**

```bash
cd TravelMind
```

2. **Create virtual environment**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` and add your API keys (see [Configuration](#configuration))

## ⚙️ Configuration

### API Keys Setup

#### 1. OpenWeatherMap API

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Add to `.env`: `OPENWEATHER_API_KEY=your_key_here`

**Features used:**
- Current Weather Data API
- Air Pollution API

#### 2. Geoapify API

1. Visit [Geoapify](https://www.geoapify.com/)
2. Sign up for a free account
3. Generate an API key
4. Add to `.env`: `GEOAPIFY_API_KEY=your_key_here`

**Features used:**
- Places API
- Geocoding API

### Environment Variables

```env
# API Keys
OPENWEATHER_API_KEY=your_openweather_api_key
GEOAPIFY_API_KEY=your_geoapify_api_key

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Output Directories
REPORTS_DIR=reports
CHARTS_DIR=charts
```

## 🚀 Usage

### Running Locally

```bash
python main.py
```

The server will start and listen for MCP protocol connections.

### Integrating with AI Agents

#### Cursor Integration

Add to your Cursor MCP configuration:

```json
{
  "mcpServers": {
    "travelmind": {
      "command": "python",
      "args": ["C:/Users/Admin/Desktop/TravelMind/main.py"],
      "env": {
        "OPENWEATHER_API_KEY": "your_key",
        "GEOAPIFY_API_KEY": "your_key"
      }
    }
  }
}
```

#### Claude Desktop Integration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "travelmind": {
      "command": "python",
      "args": ["path/to/TravelMind/main.py"]
    }
  }
}
```

## 🛠️ MCP Tools

The server exposes 8 MCP tools that AI agents can call:

### 1. `get_weather(location: str)`

Fetches current weather data for a location.

**Returns:**
- Temperature, feels like, humidity
- Wind speed, rain probability
- Weather condition and description
- Confidence score and markdown table

**Example:**
```python
result = get_weather("Pune")
# Returns: {temperature: 28.5, humidity: 65, ...}
```

### 2. `get_aqi(location: str)`

Fetches air quality index data.

**Returns:**
- AQI score and pollution level
- Health warning
- PM2.5, PM10, O3, NO2 levels
- Confidence score and markdown table

**Example:**
```python
result = get_aqi("Mumbai")
# Returns: {aqi_score: 60, pollution_level: "Moderate", ...}
```

### 3. `get_places(location: str, radius: int = 5000)`

Fetches tourist places and attractions.

**Parameters:**
- `location`: City name
- `radius`: Search radius in meters (default: 5000)

**Returns:**
- List of places by category
- Distance, name, category
- Grouped by type (attractions, museums, parks, restaurants)
- Markdown table

**Example:**
```python
result = get_places("Delhi", radius=3000)
# Returns: {total_places: 15, places: [...], ...}
```

### 4. `generate_recommendation(location: str)`

Generates comprehensive travel recommendation.

**Returns:**
- Should visit (yes/no)
- Confidence score (0-100)
- Recommendation text
- Travel advice list
- Top places to visit
- Comparison table with all scores

**Example:**
```python
result = generate_recommendation("Bangalore")
# Returns: {should_visit: True, confidence_score: 75.5, ...}
```

### 5. `generate_shopping_list(location: str)`

Generates packing/shopping checklist.

**Returns:**
- List of items with reasons
- Priority levels (high/medium/low)
- Based on weather and AQI
- Markdown table

**Example:**
```python
result = generate_shopping_list("Chennai")
# Returns: {items: [{item: "Sunscreen", reason: "High temp", priority: "high"}], ...}
```

### 6. `generate_pdf_report(location: str)`

Generates comprehensive PDF report.

**Returns:**
- PDF file path
- Report includes all data, recommendations, shopping list
- Professional formatting with tables

**Example:**
```python
result = generate_pdf_report("Pune")
# Returns: {file_path: "reports/travel_report_Pune_20240101_120000.pdf", ...}
```

### 7. `generate_chart(location: str)`

Generates visualization charts (PNG images).

**Returns:**
- Scores comparison chart
- Weather metrics chart
- Confidence gauge chart
- File paths for each chart

**Example:**
```python
result = generate_chart("Hyderabad")
# Returns: {charts: {scores_chart: "charts/scores_...", ...}, ...}
```

### 8. `get_full_analysis(location: str)`

Gets complete analysis package (all-in-one).

**Returns:**
- All of the above combined
- Complete recommendation
- Shopping list
- PDF report
- Charts

**Example:**
```python
result = get_full_analysis("Goa")
# Returns: {recommendation: {...}, shopping_list: {...}, pdf_report: {...}, charts: {...}}
```

## 📚 MCP Resources

Static reference data accessible via resource URIs:

### 1. `recommendation://rules`

Recommendation generation rules and scoring guidelines.

### 2. `recommendation://locations`

List of popular supported locations worldwide.

### 3. `recommendation://categories`

Tourist place categories and descriptions.

### 4. `recommendation://samples`

Sample output formats and examples.

## 💬 MCP Prompts

Reusable prompt templates for common scenarios:

### 1. `recommendation_prompt(location)`

Comprehensive travel recommendation prompt.

### 2. `shopping_prompt(location)`

Shopping/packing checklist prompt.

### 3. `tourist_prompt(location, category)`

Tourist places discovery prompt.

## 🔌 API Integration

### Weather API (OpenWeatherMap)

- **Endpoint**: `https://api.openweathermap.org/data/2.5/weather`
- **Rate Limit**: 60 calls/minute (free tier)
- **Data**: Temperature, humidity, wind, rain probability

### AQI API (OpenWeatherMap)

- **Endpoint**: `http://api.openweathermap.org/data/2.5/air_pollution`
- **Rate Limit**: 60 calls/minute (free tier)
- **Data**: AQI score, PM2.5, PM10, O3, NO2

### Places API (Geoapify)

- **Endpoint**: `https://api.geoapify.com/v2/places`
- **Rate Limit**: 3000 calls/day (free tier)
- **Data**: Tourist attractions, museums, parks, restaurants

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_weather_service.py
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html
```

### Test Structure

```
tests/
├── test_weather_service.py      # Weather API tests
├── test_aqi_service.py           # AQI API tests
├── test_recommendation_service.py # Recommendation logic tests
├── test_mcp_tools.py             # MCP tools tests
└── test_utils.py                 # Utilities tests
```

## 🌐 Deployment

### Railway

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login and deploy:
```bash
railway login
railway init
railway up
```

3. Set environment variables in Railway dashboard

### Render

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: travelmind-mcp
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: OPENWEATHER_API_KEY
        sync: false
      - key: GEOAPIFY_API_KEY
        sync: false
```

2. Connect GitHub repo and deploy

### Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t travelmind-mcp .
docker run -p 8000:8000 --env-file .env travelmind-mcp
```

## 📂 Project Structure

```
TravelMind/
├── main.py                      # FastMCP server entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── pytest.ini                   # Pytest configuration
├── README.md                    # This file
│
├── services/                    # API service layer
│   ├── __init__.py
│   ├── weather_service.py       # Weather API integration
│   ├── aqi_service.py           # AQI API integration
│   ├── places_service.py        # Places API integration
│   ├── recommendation_service.py # Recommendation engine
│   ├── pdf_service.py           # PDF generation
│   └── chart_service.py         # Chart generation
│
├── tools/                       # MCP tools
│   ├── __init__.py
│   └── mcp_tools.py             # Tool implementations
│
├── resources/                   # MCP resources
│   ├── __init__.py
│   └── mcp_resources.py         # Static reference data
│
├── prompts/                     # MCP prompts
│   ├── __init__.py
│   └── mcp_prompts.py           # Prompt templates
│
├── utils/                       # Utility modules
│   ├── __init__.py
│   ├── markdown_generator.py   # Markdown table generator
│   ├── confidence_calculator.py # Confidence scoring
│   ├── response_normalizer.py  # Response normalization
│   ├── logger.py                # Logging utility
│   └── retry_handler.py         # Retry logic
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration
│   ├── test_weather_service.py
│   ├── test_aqi_service.py
│   ├── test_recommendation_service.py
│   ├── test_mcp_tools.py
│   └── test_utils.py
│
├── reports/                     # Generated PDF reports (created at runtime)
└── charts/                      # Generated charts (created at runtime)
```

## 🎬 Example Flow

### User Query
```
"Should I visit Pune this evening?"
```

### AI Agent Workflow

1. **Call `get_weather("Pune")`**
   - Temperature: 28.5°C
   - Rain probability: 30%
   - Weather score: 75/100

2. **Call `get_aqi("Pune")`**
   - AQI score: 60 (Moderate)
   - AQI score: 60/100

3. **Call `get_places("Pune")`**
   - 15 places found
   - Places score: 100/100

4. **Call `generate_recommendation("Pune")`**
   - Overall confidence: 78.3%
   - Recommendation: "Good time to visit Pune"
   - Should visit: Yes

5. **Call `generate_shopping_list("Pune")`**
   - Sunscreen (high priority)
   - Water bottle (high priority)
   - Phone charger (medium priority)

6. **Call `generate_pdf_report("Pune")`**
   - PDF path: `reports/travel_report_Pune_20240101_180000.pdf`

7. **Call `generate_chart("Pune")`**
   - Scores chart: `charts/scores_Pune_20240101_180000.png`
   - Weather chart: `charts/weather_Pune_20240101_180000.png`

### Final Output

```markdown
# Travel Recommendation for Pune

## Recommendation
✅ **Yes, it's a good time to visit Pune!**

**Confidence Score**: 78.3% (High)

## Weather Summary
| Metric          | Value  |
|-----------------|--------|
| Temperature     | 28.5°C |
| Rain Probability| 30%    |
| Humidity        | 65%    |

## Air Quality
| Metric          | Value    |
|-----------------|----------|
| AQI Score       | 60       |
| Level           | Moderate |

## Travel Advice
- Stay hydrated and wear light clothing
- Enjoy your visit!

## Shopping Checklist
- ✅ Sunscreen (High temp: 28.5°C)
- ✅ Water bottle (Stay hydrated)
- ✅ Phone charger (Essential)

## Top Places to Visit
1. Shaniwar Wada (500m)
2. Aga Khan Palace (1.2km)
3. Osho Garden (2.5km)

📄 **PDF Report**: [Download](reports/travel_report_Pune_20240101_180000.pdf)
📊 **Charts**: Available in charts directory
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [FastMCP](https://github.com/jlowin/fastmcp) for MCP server framework
- [OpenWeatherMap](https://openweathermap.org/) for weather and AQI data
- [Geoapify](https://www.geoapify.com/) for places data

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for AI agents and travel enthusiasts**
