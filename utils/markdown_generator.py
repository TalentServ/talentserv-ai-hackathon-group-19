"""
Markdown table generator utility
"""
from typing import List, Dict, Any


class MarkdownTableGenerator:
    
    @staticmethod
    def generate_weather_table(weather_data: Dict) -> str:
        """Generate markdown table for weather data"""
        headers = ["Metric", "Value", "Source"]
        rows = [
            ["Temperature", f"{weather_data.get('temperature', 'N/A')}°C", weather_data.get('source', 'N/A')],
            ["Feels Like", f"{weather_data.get('feels_like', 'N/A')}°C", ""],
            ["Humidity", f"{weather_data.get('humidity', 'N/A')}%", ""],
            ["Wind Speed", f"{weather_data.get('wind_speed', 'N/A')} m/s", ""],
            ["Rain Probability", f"{weather_data.get('rain_probability', 'N/A')}%", ""],
            ["Condition", weather_data.get('weather_condition', 'N/A'), ""],
            ["Confidence", weather_data.get('confidence', 'N/A').title(), ""]
        ]
        
        return MarkdownTableGenerator._create_table(headers, rows)
    
    @staticmethod
    def generate_aqi_table(aqi_data: Dict) -> str:
        """Generate markdown table for AQI data"""
        headers = ["Metric", "Value", "Source"]
        rows = [
            ["AQI Score", str(aqi_data.get('aqi_score', 'N/A')), aqi_data.get('source', 'N/A')],
            ["Pollution Level", aqi_data.get('pollution_level', 'N/A'), ""],
            ["Health Warning", aqi_data.get('health_warning', 'N/A'), ""],
            ["PM2.5", f"{aqi_data.get('pm2_5', 'N/A')}", ""],
            ["PM10", f"{aqi_data.get('pm10', 'N/A')}", ""],
            ["Confidence", aqi_data.get('confidence', 'N/A').title(), ""]
        ]
        
        return MarkdownTableGenerator._create_table(headers, rows)
    
    @staticmethod
    def generate_places_table(places: List[Dict], limit: int = 10) -> str:
        """Generate markdown table for tourist places"""
        headers = ["Place Name", "Category", "Distance (m)"]
        rows = []
        
        for place in places[:limit]:
            rows.append([
                place.get('name', 'Unknown'),
                place.get('category', 'N/A'),
                str(round(place.get('distance', 0)))
            ])
        
        if not rows:
            rows.append(["No places available", "", ""])
        
        return MarkdownTableGenerator._create_table(headers, rows)
    
    @staticmethod
    def generate_shopping_table(shopping_list: Dict) -> str:
        """Generate markdown table for shopping checklist"""
        headers = ["Item", "Reason", "Priority"]
        rows = []
        
        for item in shopping_list.get('items', []):
            rows.append([
                item.get('item', ''),
                item.get('reason', ''),
                item.get('priority', '').upper()
            ])
        
        if not rows:
            rows.append(["No items", "", ""])
        
        return MarkdownTableGenerator._create_table(headers, rows)
    
    @staticmethod
    def generate_comparison_table(weather_data: Dict, aqi_data: Dict, 
                                 recommendation: Dict) -> str:
        """Generate comparison table with all metrics"""
        headers = ["Category", "Score", "Status", "Confidence"]
        rows = [
            ["Weather", f"{recommendation.get('weather_score', 0):.1f}%", 
             weather_data.get('status', 'N/A'), weather_data.get('confidence', 'N/A').title()],
            ["Air Quality", f"{recommendation.get('aqi_score', 0):.1f}%", 
             aqi_data.get('status', 'N/A'), aqi_data.get('confidence', 'N/A').title()],
            ["Overall", f"{recommendation.get('confidence_score', 0):.1f}%", 
             "success", recommendation.get('confidence_level', 'N/A')]
        ]
        
        return MarkdownTableGenerator._create_table(headers, rows)
    
    @staticmethod
    def _create_table(headers: List[str], rows: List[List[str]]) -> str:
        """Create markdown table from headers and rows"""
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Create table
        lines = []
        
        # Header
        header_line = "| " + " | ".join(
            h.ljust(col_widths[i]) for i, h in enumerate(headers)
        ) + " |"
        lines.append(header_line)
        
        # Separator
        separator = "| " + " | ".join("-" * w for w in col_widths) + " |"
        lines.append(separator)
        
        # Rows
        for row in rows:
            row_line = "| " + " | ".join(
                str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)
            ) + " |"
            lines.append(row_line)
        
        return "\n".join(lines)
