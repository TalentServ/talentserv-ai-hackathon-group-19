"""
Chart generation service using matplotlib
"""
import os
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
from typing import Dict, Any, List

# Use non-interactive backend
matplotlib.use('Agg')


class ChartService:
    def __init__(self):
        self.charts_dir = os.getenv("CHARTS_DIR", "charts")
        os.makedirs(self.charts_dir, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def generate_chart(self, weather_data: Dict, aqi_data: Dict, 
                      recommendation: Dict) -> Dict[str, Any]:
        """
        Generate visualization charts with inline display support
        
        Args:
            weather_data: Weather information
            aqi_data: Air quality information
            recommendation: Recommendation data
            
        Returns:
            Chart metadata with file paths and base64 encoded images
        """
        try:
            location = weather_data.get("location", "Unknown")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Generate multiple charts
            charts = {}
            charts_base64 = {}
            
            # 1. Scores comparison chart
            scores_path, scores_b64 = self._generate_scores_chart(
                recommendation, location, timestamp
            )
            charts['scores_chart'] = scores_path
            charts_base64['scores_chart'] = scores_b64
            
            # 2. Weather metrics chart
            weather_path, weather_b64 = self._generate_weather_chart(
                weather_data, location, timestamp
            )
            charts['weather_chart'] = weather_path
            charts_base64['weather_chart'] = weather_b64
            
            # 3. Confidence gauge chart
            confidence_path, confidence_b64 = self._generate_confidence_gauge(
                recommendation, location, timestamp
            )
            charts['confidence_chart'] = confidence_path
            charts_base64['confidence_chart'] = confidence_b64
            
            return {
                "status": "success",
                "charts": charts,
                "charts_base64": charts_base64,
                "location": location,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "charts": {},
                "charts_base64": {},
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _generate_scores_chart(self, recommendation: Dict, location: str, 
                              timestamp: str) -> tuple:
        """Generate bar chart comparing different scores"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = ['Weather', 'Air Quality', 'Places', 'Overall']
        scores = [
            recommendation.get('weather_score', 0),
            recommendation.get('aqi_score', 0),
            recommendation.get('places_score', 0),
            recommendation.get('confidence_score', 0)
        ]
        
        colors_list = ['#1a73e8', '#34a853', '#fbbc04', '#ea4335']
        bars = ax.bar(categories, scores, color=colors_list, alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Score', fontsize=12, fontweight='bold')
        ax.set_title(f'Recommendation Scores - {location}', 
                    fontsize=14, fontweight='bold')
        ax.set_ylim(0, 110)
        ax.grid(axis='y', alpha=0.3)
        
        # Save chart to file
        filename = f"scores_{location}_{timestamp}.png"
        filepath = os.path.join(self.charts_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        
        # Also save to base64 for inline display
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        buffer.close()
        plt.close()
        
        return filepath, image_base64
    
    def _generate_weather_chart(self, weather_data: Dict, location: str, 
                               timestamp: str) -> tuple:
        """Generate weather metrics visualization"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Temperature gauge
        temp = weather_data.get('temperature', 0)
        feels_like = weather_data.get('feels_like', 0)
        
        ax1.barh(['Temperature', 'Feels Like'], [temp, feels_like], 
                color=['#1a73e8', '#34a853'], alpha=0.8)
        ax1.set_xlabel('Temperature (°C)', fontweight='bold')
        ax1.set_title('Temperature Metrics', fontweight='bold')
        ax1.set_xlim(0, 50)
        
        for i, v in enumerate([temp, feels_like]):
            ax1.text(v + 1, i, f'{v}°C', va='center', fontweight='bold')
        
        # Other metrics
        metrics = {
            'Humidity': weather_data.get('humidity', 0),
            'Rain Prob': weather_data.get('rain_probability', 0),
            'Wind Speed': weather_data.get('wind_speed', 0) * 3.6  # Convert to km/h
        }
        
        colors_map = {'Humidity': '#fbbc04', 'Rain Prob': '#4285f4', 
                     'Wind Speed': '#ea4335'}
        
        bars = ax2.bar(metrics.keys(), metrics.values(), 
                      color=[colors_map[k] for k in metrics.keys()], alpha=0.8)
        
        ax2.set_ylabel('Value', fontweight='bold')
        ax2.set_title('Weather Metrics', fontweight='bold')
        ax2.set_ylim(0, 110)
        
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontweight='bold')
        
        fig.suptitle(f'Weather Analysis - {location}', fontsize=14, 
                    fontweight='bold', y=1.02)
        
        # Save chart to file
        filename = f"weather_{location}_{timestamp}.png"
        filepath = os.path.join(self.charts_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        
        # Also save to base64 for inline display
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        buffer.close()
        plt.close()
        
        return filepath, image_base64
    
    def _generate_confidence_gauge(self, recommendation: Dict, location: str, 
                                  timestamp: str) -> tuple:
        """Generate confidence gauge visualization"""
        fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'projection': 'polar'})
        
        confidence = recommendation.get('confidence_score', 0)
        
        # Create gauge
        theta = [0, confidence * 1.8 * 3.14159 / 180]  # Convert to radians
        radii = [0, 1]
        width = 0.4
        
        # Color based on confidence
        if confidence >= 80:
            color = '#34a853'
        elif confidence >= 60:
            color = '#fbbc04'
        elif confidence >= 40:
            color = '#ff6d01'
        else:
            color = '#ea4335'
        
        bars = ax.bar(theta[1], radii[1], width=width, bottom=0.0, 
                     color=color, alpha=0.8)
        
        # Add confidence text
        ax.text(0, 0, f'{confidence:.1f}%', 
               ha='center', va='center', fontsize=24, fontweight='bold')
        ax.text(0, -0.3, recommendation.get('confidence_level', ''), 
               ha='center', va='center', fontsize=14)
        
        ax.set_ylim(0, 1)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['polar'].set_visible(False)
        
        plt.title(f'Confidence Score - {location}', fontsize=14, 
                 fontweight='bold', pad=20)
        
        # Save chart to file
        filename = f"confidence_{location}_{timestamp}.png"
        filepath = os.path.join(self.charts_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        
        # Also save to base64 for inline display
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        buffer.close()
        plt.close()
        
        return filepath, image_base64
