import json
import sys

# Read the JSON file
with open(r'C:\Users\Admin\.cursor\projects\c-Users-Admin-Desktop-TravelMind\agent-tools\a233e8de-fe26-444e-acd4-48335352c3d7.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('='*70)
print('TRAVEL RECOMMENDATION FOR MUMBAI')
print('='*70)
print(f'\nShould Visit: {"YES" if data["should_visit"] else "NO"}')
print(f'Confidence: {data["confidence_score"]}% ({data["confidence_level"]})')
print(f'\nRecommendation: {data["recommendation"]}')

print(f'\nTRAVEL ADVICE:')
for advice in data['travel_advice']:
    print(f'  - {advice}')

# Weather info
if 'weather_data' in data:
    weather = data['weather_data']
    print(f'\nWEATHER:')
    print(f'  Temperature: {weather.get("temperature", "N/A")}°C (Feels like: {weather.get("feels_like", "N/A")}°C)')
    print(f'  Humidity: {weather.get("humidity", "N/A")}%')
    print(f'  Wind Speed: {weather.get("wind_speed", "N/A")} m/s')
    print(f'  Condition: {weather.get("condition", "N/A")}')
    print(f'  Weather Score: {weather.get("weather_score", "N/A")}/100')

# AQI info
if 'aqi_data' in data:
    aqi = data['aqi_data']
    print(f'\nAIR QUALITY:')
    print(f'  AQI Score: {aqi.get("aqi_score", "N/A")}')
    print(f'  Level: {aqi.get("pollution_level", "N/A")}')
    print(f'  AQI Score: {aqi.get("aqi_score_normalized", "N/A")}/100')
    print(f'  Health Warning: {aqi.get("health_warning", "N/A")}')

# Top places
print(f'\nTOP 10 PLACES TO VISIT:')
for i, place in enumerate(data['top_places'][:10], 1):
    name = place.get('name', 'Unknown')
    category = place.get('category', 'Unknown')
    rating = place.get('rating')
    rating_str = f" (Rating: {rating})" if rating else ""
    print(f'  {i}. {name} ({category}){rating_str}')

# Shopping list
if 'shopping_list' in data:
    print(f'\nPACKING CHECKLIST:')
    for item in data['shopping_list'].get('items', [])[:8]:
        priority = item.get('priority', 'medium')
        priority_str = f'[{priority.upper()}]'
        print(f'  {priority_str} {item.get("item", "Unknown")} - {item.get("reason", "")}')

# PDF and charts
if 'pdf_report' in data:
    print(f'\nPDF REPORT: {data["pdf_report"].get("file_path", "N/A")}')

if 'charts' in data:
    charts = data['charts'].get('charts', {})
    if charts:
        print(f'\nCHARTS GENERATED:')
        for chart_name, chart_path in charts.items():
            if chart_path:
                print(f'  - {chart_name}: {chart_path}')

print('\n' + '='*70)
