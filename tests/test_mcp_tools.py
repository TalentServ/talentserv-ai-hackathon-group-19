"""
Tests for MCP tools
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from tools.mcp_tools import MCPTools


class TestMCPTools:
    
    def setup_method(self):
        """Setup test fixtures"""
        self.tools = MCPTools()
    
    @patch('tools.mcp_tools.WeatherService')
    def test_get_weather(self, mock_weather_service):
        """Test get_weather tool"""
        mock_service = Mock()
        mock_service.get_weather.return_value = {
            "location": "Pune",
            "temperature": 28.5,
            "status": "success"
        }
        mock_weather_service.return_value = mock_service
        
        tools = MCPTools()
        result = tools.get_weather("Pune")
        
        assert "markdown_table" in result
        assert result["status"] == "success"
    
    @patch('tools.mcp_tools.AQIService')
    def test_get_aqi(self, mock_aqi_service):
        """Test get_aqi tool"""
        mock_service = Mock()
        mock_service.get_aqi.return_value = {
            "location": "Pune",
            "aqi_score": 40,
            "status": "success"
        }
        mock_aqi_service.return_value = mock_service
        
        tools = MCPTools()
        result = tools.get_aqi("Pune")
        
        assert "markdown_table" in result
        assert result["status"] == "success"
    
    @patch('tools.mcp_tools.PlacesService')
    def test_get_places(self, mock_places_service):
        """Test get_places tool"""
        mock_service = Mock()
        mock_service.get_places.return_value = {
            "location": "Pune",
            "total_places": 10,
            "places": [],
            "status": "success"
        }
        mock_places_service.return_value = mock_service
        
        tools = MCPTools()
        result = tools.get_places("Pune")
        
        assert "markdown_table" in result
        assert result["status"] == "success"
    
    @patch('tools.mcp_tools.WeatherService')
    @patch('tools.mcp_tools.AQIService')
    @patch('tools.mcp_tools.PlacesService')
    @patch('tools.mcp_tools.RecommendationService')
    def test_generate_recommendation(self, mock_rec_service, mock_places_service, 
                                    mock_aqi_service, mock_weather_service):
        """Test generate_recommendation tool"""
        # Setup mocks
        mock_weather_service.return_value.get_weather.return_value = {
            "location": "Pune", "temperature": 28.5, "status": "success"
        }
        mock_aqi_service.return_value.get_aqi.return_value = {
            "location": "Pune", "aqi_score": 40, "status": "success"
        }
        mock_places_service.return_value.get_places.return_value = {
            "location": "Pune", "total_places": 10, "places": [], "status": "success"
        }
        mock_rec_service.return_value.generate_recommendation.return_value = {
            "location": "Pune",
            "confidence_score": 75.0,
            "recommendation": "Good time to visit",
            "status": "success"
        }
        
        tools = MCPTools()
        result = tools.generate_recommendation("Pune")
        
        assert "comparison_table" in result
        assert "source_data" in result
        assert result["status"] == "success"
    
    @patch('tools.mcp_tools.PDFService')
    def test_generate_pdf_report(self, mock_pdf_service):
        """Test PDF report generation"""
        mock_service = Mock()
        mock_service.generate_pdf_report.return_value = {
            "status": "success",
            "file_path": "reports/test.pdf"
        }
        
        # Mock all other services
        with patch('tools.mcp_tools.WeatherService'), \
             patch('tools.mcp_tools.AQIService'), \
             patch('tools.mcp_tools.PlacesService'), \
             patch('tools.mcp_tools.RecommendationService'):
            
            self.tools.pdf_service = mock_service
            result = self.tools.generate_pdf_report("Pune")
            
            assert result["status"] == "success"
            assert "file_path" in result
    
    @patch('tools.mcp_tools.ChartService')
    def test_generate_chart(self, mock_chart_service):
        """Test chart generation"""
        mock_service = Mock()
        mock_service.generate_chart.return_value = {
            "status": "success",
            "charts": {"scores_chart": "charts/test.png"}
        }
        
        # Mock all other services
        with patch('tools.mcp_tools.WeatherService'), \
             patch('tools.mcp_tools.AQIService'), \
             patch('tools.mcp_tools.PlacesService'), \
             patch('tools.mcp_tools.RecommendationService'):
            
            self.tools.chart_service = mock_service
            result = self.tools.generate_chart("Pune")
            
            assert result["status"] == "success"
            assert "charts" in result
