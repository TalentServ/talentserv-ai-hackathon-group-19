"""
PDF report generation service using reportlab
"""
import os
from datetime import datetime
from typing import Dict, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class PDFService:
    def __init__(self):
        self.reports_dir = os.getenv("REPORTS_DIR", "reports")
        os.makedirs(self.reports_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34a853'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def generate_pdf_report(self, weather_data: Dict, aqi_data: Dict, 
                          places_data: Dict, recommendation: Dict, 
                          shopping_list: Dict) -> Dict[str, Any]:
        """
        Generate comprehensive PDF report
        
        Args:
            weather_data: Weather information
            aqi_data: Air quality information
            places_data: Tourist places information
            recommendation: Recommendation data
            shopping_list: Shopping checklist
            
        Returns:
            Report metadata with file path
        """
        try:
            location = weather_data.get("location", "Unknown")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"travel_report_{location}_{timestamp}.pdf"
            filepath = os.path.join(self.reports_dir, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            story = []
            
            # Title
            title = Paragraph(f"TravelMind Report: {location}", self.styles['CustomTitle'])
            story.append(title)
            story.append(Spacer(1, 0.2*inch))
            
            # Generated date
            date_text = Paragraph(
                f"<i>Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}</i>",
                self.styles['Normal']
            )
            story.append(date_text)
            story.append(Spacer(1, 0.3*inch))
            
            # Recommendation Summary
            story.append(Paragraph("Recommendation Summary", self.styles['SectionHeader']))
            rec_text = f"""
            <b>Should Visit:</b> {'Yes' if recommendation.get('should_visit') else 'No'}<br/>
            <b>Confidence Score:</b> {recommendation.get('confidence_score')}% ({recommendation.get('confidence_level')})<br/>
            <b>Recommendation:</b> {recommendation.get('recommendation')}<br/>
            <b>Explanation:</b> {recommendation.get('explanation')}
            """
            story.append(Paragraph(rec_text, self.styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Weather Summary
            story.append(Paragraph("Weather Summary", self.styles['SectionHeader']))
            story.append(self._create_weather_table(weather_data))
            story.append(Spacer(1, 0.2*inch))
            
            # AQI Summary
            story.append(Paragraph("Air Quality Index", self.styles['SectionHeader']))
            story.append(self._create_aqi_table(aqi_data))
            story.append(Spacer(1, 0.2*inch))
            
            # Travel Advice
            story.append(Paragraph("Travel Advice", self.styles['SectionHeader']))
            advice_list = recommendation.get('travel_advice', [])
            for advice in advice_list:
                story.append(Paragraph(f"• {advice}", self.styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Shopping Checklist
            story.append(Paragraph("Shopping Checklist", self.styles['SectionHeader']))
            story.append(self._create_shopping_table(shopping_list))
            story.append(Spacer(1, 0.2*inch))
            
            # Top Places
            story.append(Paragraph("Top Places to Visit", self.styles['SectionHeader']))
            story.append(self._create_places_table(recommendation.get('top_places', [])))
            
            # Build PDF
            doc.build(story)
            
            return {
                "status": "success",
                "file_path": filepath,
                "filename": filename,
                "location": location,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "file_path": None,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _create_weather_table(self, weather_data: Dict) -> Table:
        """Create weather summary table"""
        data = [
            ['Metric', 'Value'],
            ['Temperature', f"{weather_data.get('temperature', 'N/A')}°C"],
            ['Feels Like', f"{weather_data.get('feels_like', 'N/A')}°C"],
            ['Humidity', f"{weather_data.get('humidity', 'N/A')}%"],
            ['Wind Speed', f"{weather_data.get('wind_speed', 'N/A')} m/s"],
            ['Rain Probability', f"{weather_data.get('rain_probability', 'N/A')}%"],
            ['Condition', weather_data.get('weather_condition', 'N/A')]
        ]
        
        table = Table(data, colWidths=[2.5*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_aqi_table(self, aqi_data: Dict) -> Table:
        """Create AQI summary table"""
        data = [
            ['Metric', 'Value'],
            ['AQI Score', str(aqi_data.get('aqi_score', 'N/A'))],
            ['Pollution Level', aqi_data.get('pollution_level', 'N/A')],
            ['Health Warning', aqi_data.get('health_warning', 'N/A')]
        ]
        
        table = Table(data, colWidths=[2.5*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34a853')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_shopping_table(self, shopping_list: Dict) -> Table:
        """Create shopping checklist table"""
        data = [['Item', 'Reason', 'Priority']]
        
        for item_data in shopping_list.get('items', []):
            data.append([
                item_data.get('item', ''),
                item_data.get('reason', ''),
                item_data.get('priority', '').upper()
            ])
        
        table = Table(data, colWidths=[1.5*inch, 3*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fbbc04')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_places_table(self, places: list) -> Table:
        """Create top places table with clickable blue links"""
        from reportlab.platypus import Paragraph
        
        data = [['Place Name', 'Category', 'Rating', 'View on Map']]
        
        # Style for links
        link_style = ParagraphStyle(
            'Link',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#0000EE'),
            underline=True
        )
        
        for place in places:
            rating_text = f"{place.get('rating', 'N/A')}/5" if place.get('rating') else "N/A"
            link = place.get('google_maps_link', '')
            
            # Create clickable link paragraph
            if link:
                link_para = Paragraph(
                    f'<a href="{link}" color="blue">Open in Maps</a>',
                    link_style
                )
            else:
                link_para = "N/A"
            
            data.append([
                Paragraph(place.get('name', 'Unknown'), self.styles['Normal']),
                place.get('category', 'N/A'),
                rating_text,
                link_para
            ])
        
        if len(data) == 1:
            data.append(['No places available', '', '', ''])
        
        table = Table(data, colWidths=[2.5*inch, 1.5*inch, 0.7*inch, 1.3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea4335')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('WORDWRAP', (0, 0), (-1, -1), True)
        ]))
        
        return table
