# Quick Start Guide

Get TravelMind MCP Server up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.11 or higher installed
- [ ] pip package manager
- [ ] Git (optional, for cloning)

## Step 1: Get the Code

Download or clone the TravelMind project to your local machine.

## Step 2: Setup Virtual Environment

```bash
# Navigate to project directory
cd TravelMind

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI & FastMCP
- requests (for API calls)
- pandas (data processing)
- matplotlib (charts)
- reportlab (PDF generation)
- pytest (testing)

## Step 4: Get API Keys

### OpenWeatherMap (Required)

1. Go to [https://openweathermap.org/api](https://openweathermap.org/api)
2. Click "Sign Up" (top right)
3. Create free account
4. Go to API Keys section
5. Copy your API key

### Geoapify (Required)

1. Go to [https://www.geoapify.com/](https://www.geoapify.com/)
2. Click "Get Started Free"
3. Create account
4. Go to API Keys
5. Copy your API key

## Step 5: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# Windows: notepad .env
# macOS/Linux: nano .env
```

Your `.env` should look like:

```env
OPENWEATHER_API_KEY=your_actual_openweather_key_here
GEOAPIFY_API_KEY=your_actual_geoapify_key_here
DEBUG=True
```

## Step 6: Test the Setup

Run the example script to verify everything works:

```bash
python example_usage.py
```

You should see output like:

```
============================================================
TravelMind Example - Analyzing Pune
============================================================

1. Fetching Weather Data...
   Temperature: 28.5°C
   Rain Probability: 30%
   Status: success

2. Fetching AQI Data...
   AQI Score: 60
   Pollution Level: Moderate
   Status: success
...
```

## Step 7: Run the MCP Server

```bash
python main.py
```

You should see:

```
Starting TravelMind MCP Server...
All required environment variables are set
Created directories: reports, charts
TravelMind MCP Server is ready!
Available tools: get_weather, get_aqi, get_places, ...
```

## Step 8: Integrate with AI Agent

### For Cursor IDE

1. Open Cursor Settings
2. Go to MCP Configuration
3. Add TravelMind server:

```json
{
  "mcpServers": {
    "travelmind": {
      "command": "python",
      "args": ["C:/Users/Admin/Desktop/TravelMind/main.py"]
    }
  }
}
```

4. Restart Cursor
5. You can now use TravelMind tools in your AI conversations!

### For Claude Desktop

Add to your `claude_desktop_config.json`:

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

## Step 9: Test with AI Agent

Try asking your AI agent:

```
"Should I visit Pune today? Give me a complete analysis."
```

The AI will use TravelMind's MCP tools to:
1. Fetch weather data
2. Fetch air quality data
3. Find tourist places
4. Generate recommendation
5. Create shopping list
6. Generate PDF report
7. Create charts

## Troubleshooting

### "Module not found" error

```bash
# Make sure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

### "Missing API key" error

Check your `.env` file:
- Make sure API keys are correct (no spaces, quotes)
- Make sure `.env` is in the project root
- Try restarting the server after editing `.env`

### "API timeout" or "API error"

- Check your internet connection
- Verify API keys are valid and active
- Check API rate limits (free tier has limits)
- Try with a different location

### Tests failing

```bash
# Run tests with verbose output
pytest -v

# If some tests fail due to missing API keys, that's okay
# The core functionality should still work
```

## What's Next?

1. **Read the full README**: Check `README.md` for detailed documentation
2. **Run tests**: `pytest` to see all tests pass
3. **Explore the code**: Browse `services/`, `tools/`, `utils/` directories
4. **Try different locations**: Test with your favorite cities
5. **Check generated files**: Look in `reports/` and `charts/` directories
6. **Customize**: Modify scoring rules, add new features

## Common Commands

```bash
# Run MCP server
python main.py

# Run example script
python example_usage.py

# Run tests
pytest

# Run specific test file
pytest tests/test_weather_service.py

# Install new dependency
pip install package-name
pip freeze > requirements.txt
```

## Get Help

- Check `README.md` for detailed docs
- Check `CONTRIBUTING.md` for development guide
- Open an issue on GitHub
- Review the code comments and docstrings

## Success Checklist

- [x] Python installed
- [x] Dependencies installed
- [x] API keys configured
- [x] Example script runs successfully
- [x] MCP server starts without errors
- [x] Integrated with AI agent (Cursor/Claude)
- [x] AI agent can use TravelMind tools

Congratulations! You're all set with TravelMind MCP Server! 🎉

---

**Next Steps**: Try generating a full travel report for your city and see the magic happen!
