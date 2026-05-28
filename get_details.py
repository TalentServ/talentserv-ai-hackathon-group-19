import json

with open(r'C:\Users\Admin\.cursor\projects\c-Users-Admin-Desktop-TravelMind\agent-tools\a233e8de-fe26-444e-acd4-48335352c3d7.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

src = data.get('source_data', {})
weather = src.get('weather', {})
aqi = src.get('aqi', {})

print('WEATHER DETAILS:')
print(f'  Temperature: {weather.get("temperature", "N/A")}C')
print(f'  Feels Like: {weather.get("feels_like", "N/A")}C')
print(f'  Humidity: {weather.get("humidity", "N/A")}%')
print(f'  Wind Speed: {weather.get("wind_speed", "N/A")} m/s')
print(f'  Rain Probability: {weather.get("rain_probability", "N/A")}%')
print(f'  Condition: {weather.get("condition", "N/A")}')
print(f'  Description: {weather.get("description", "N/A")}')

print('\nAIR QUALITY DETAILS:')
print(f'  AQI Score: {aqi.get("aqi_score", "N/A")}')
print(f'  Pollution Level: {aqi.get("pollution_level", "N/A")}')
print(f'  Health Warning: {aqi.get("health_warning", "N/A")}')

print('\nPLACES:')
places = src.get('places', {})
print(f'  Total Places: {places.get("total_places", 0)}')
print(f'  Attractions: {places.get("attractions_count", 0)}')
print(f'  Museums: {places.get("museums_count", 0)}')
print(f'  Parks: {places.get("parks_count", 0)}')
print(f'  Restaurants: {places.get("restaurants_count", 0)}')
