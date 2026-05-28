# Contributing to TravelMind

Thank you for your interest in contributing to TravelMind! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a positive environment

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version)
   - Error messages and logs

### Suggesting Features

1. Check if the feature has been suggested
2. Create a new issue with:
   - Clear use case
   - Expected behavior
   - Potential implementation approach
   - Benefits to users

### Code Contributions

#### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/TravelMind.git
cd TravelMind

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Add your API keys to .env
```

#### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow existing code style
   - Add tests for new features
   - Update documentation
   - Add docstrings to functions

3. **Run tests**
   ```bash
   pytest
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide clear description
   - Reference related issues
   - Include screenshots if applicable

## Coding Standards

### Python Style Guide

- Follow PEP 8 style guide
- Use type hints
- Write descriptive variable names
- Keep functions focused and small
- Add docstrings to all functions/classes

### Example

```python
def calculate_score(temperature: float, humidity: int) -> float:
    """
    Calculate comfort score based on temperature and humidity
    
    Args:
        temperature: Temperature in Celsius
        humidity: Humidity percentage (0-100)
        
    Returns:
        Comfort score (0-100)
    """
    # Implementation here
    pass
```

### Testing Standards

- Write tests for all new features
- Maintain test coverage above 80%
- Use descriptive test names
- Test both success and error cases
- Use mocks for external API calls

### Example

```python
def test_weather_service_success():
    """Test successful weather data fetch"""
    # Arrange
    service = WeatherService()
    
    # Act
    result = service.get_weather("Pune")
    
    # Assert
    assert result["status"] == "success"
    assert "temperature" in result
```

## Project Structure Guidelines

### Adding New Services

```python
# services/new_service.py
class NewService:
    def __init__(self):
        # Initialize service
        pass
    
    def fetch_data(self, location: str) -> dict:
        """Fetch data from API"""
        # Implementation
        pass
```

### Adding New Tools

```python
# tools/mcp_tools.py
@mcp.tool()
def new_tool(location: str) -> dict:
    """
    Tool description
    
    Args:
        location: Location parameter
        
    Returns:
        Result dictionary
    """
    # Implementation
    pass
```

### Adding New Utilities

```python
# utils/new_utility.py
class NewUtility:
    @staticmethod
    def process_data(data: dict) -> dict:
        """Process data"""
        # Implementation
        pass
```

## Documentation

- Update README.md for user-facing changes
- Update docstrings for code changes
- Add examples for new features
- Update CHANGELOG.md

## Review Process

1. Maintainers will review your PR
2. Address feedback and make changes
3. Once approved, your PR will be merged
4. Your contribution will be credited

## Questions?

- Open an issue for questions
- Tag maintainers for urgent matters
- Be patient and respectful

Thank you for contributing to TravelMind!
