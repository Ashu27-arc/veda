"""
Weather API Integration
Get real-time weather updates
"""

import requests
from python_backend.logger import log_info, log_error

# Primary API - wttr.in (free, no key required)
WEATHER_API_URL = "https://wttr.in/{}?format=j1"

# Backup API - Open-Meteo (free, no key required, faster)
BACKUP_API_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"

def get_weather_backup(city=""):
    """Backup weather API using Open-Meteo (faster and more reliable)"""
    try:
        # Get coordinates for the city
        if not city or city == "auto:ip":
            # Use a default location or IP-based location
            # For now, we'll use a popular city as fallback
            lat, lon = 28.6139, 77.2090  # Delhi coordinates as default
            location_name = "Current Location"
        else:
            # Geocode the city name
            log_info(f"Geocoding city: {city}")
            geo_response = requests.get(
                GEOCODING_API_URL,
                params={"name": city, "count": 1, "language": "en", "format": "json"},
                timeout=5
            )
            
            if geo_response.status_code != 200 or not geo_response.json().get("results"):
                log_error(f"Geocoding failed for: {city}")
                return None
            
            geo_data = geo_response.json()["results"][0]
            lat = geo_data["latitude"]
            lon = geo_data["longitude"]
            location_name = f"{geo_data['name']}, {geo_data.get('country', '')}"
        
        # Get weather data
        log_info(f"Fetching weather for coordinates: {lat}, {lon}")
        weather_response = requests.get(
            BACKUP_API_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "timezone": "auto"
            },
            timeout=5
        )
        
        if weather_response.status_code != 200:
            log_error(f"Weather API error: {weather_response.status_code}")
            return None
        
        data = weather_response.json()
        current = data["current_weather"]
        
        # Map weather codes to conditions
        weather_codes = {
            0: "Clear", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Fog", 51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
            61: "Light rain", 63: "Rain", 65: "Heavy rain", 71: "Light snow", 
            73: "Snow", 75: "Heavy snow", 95: "Thunderstorm"
        }
        
        condition = weather_codes.get(current["weathercode"], "Unknown")
        
        weather_info = {
            'location': location_name,
            'temperature': str(int(current['temperature'])),
            'feels_like': str(int(current['temperature'] - 2)),  # Approximate
            'condition': condition,
            'humidity': "N/A",
            'wind_speed': str(int(current['windspeed'])),
            'wind_dir': "N/A"
        }
        
        log_info(f"Weather fetched successfully (backup API): {location_name}")
        return weather_info
        
    except Exception as e:
        log_error(f"Backup weather API error: {e}")
        return None
def get_weather(city=""):
    """Get weather information for a city (with fallback to backup API)"""
    try:
        # If no city specified, try to get location-based weather
        if not city:
            city = "auto:ip"  # Auto-detect location from IP
        
        log_info(f"Fetching weather for: {city}")
        
        # Make request to weather API with shorter timeout
        response = requests.get(
            WEATHER_API_URL.format(city),
            timeout=5
        )
        
        if response.status_code != 200:
            log_error(f"Weather API error: {response.status_code}")
            # Try backup API
            log_info("Trying backup weather API...")
            return get_weather_backup(city)
        
        data = response.json()
        
        # Extract weather information
        current = data['current_condition'][0]
        location = data['nearest_area'][0]
        
        weather_info = {
            'location': f"{location['areaName'][0]['value']}, {location['country'][0]['value']}",
            'temperature': current['temp_C'],
            'feels_like': current['FeelsLikeC'],
            'condition': current['weatherDesc'][0]['value'],
            'humidity': current['humidity'],
            'wind_speed': current['windspeedKmph'],
            'wind_dir': current['winddir16Point']
        }
        
        log_info(f"Weather fetched successfully: {weather_info['location']}")
        return weather_info
        
    except requests.exceptions.Timeout:
        log_error("Weather API timeout - trying backup API")
        return get_weather_backup(city)
    except requests.exceptions.ConnectionError as e:
        log_error(f"Weather API connection error: {e} - trying backup API")
        return get_weather_backup(city)
    except requests.exceptions.RequestException as e:
        log_error(f"Weather API request error: {e} - trying backup API")
        return get_weather_backup(city)
    except KeyError as e:
        log_error(f"Weather data parsing error - missing key: {e}")
        return get_weather_backup(city)
    except Exception as e:
        log_error(f"Unexpected weather error: {e}")
        return get_weather_backup(city)

def format_weather_response(weather_info, language='english'):
    """Format weather information into a readable response"""
    if not weather_info:
        if language == 'hinglish':
            return "माफ़ कीजिए, मौसम की जानकारी अभी उपलब्ध नहीं है। इंटरनेट कनेक्शन चेक करें।"
        return "Sorry, I couldn't fetch the weather information. Please check your internet connection."
    
    temp = weather_info['temperature']
    feels = weather_info['feels_like']
    condition = weather_info['condition']
    location = weather_info['location']
    humidity = weather_info['humidity']
    wind = weather_info['wind_speed']
    
    # Translate weather conditions to Hindi
    condition_hindi = {
        'Clear': 'साफ़',
        'Sunny': 'धूप',
        'Mainly clear': 'ज़्यादातर साफ़',
        'Partly cloudy': 'आंशिक बादल',
        'Cloudy': 'बादल',
        'Overcast': 'घने बादल',
        'Mist': 'धुंध',
        'Fog': 'कोहरा',
        'Light rain': 'हल्की बारिश',
        'Light drizzle': 'हल्की बूंदाबांदी',
        'Drizzle': 'बूंदाबांदी',
        'Heavy drizzle': 'भारी बूंदाबांदी',
        'Rain': 'बारिश',
        'Heavy rain': 'भारी बारिश',
        'Thunderstorm': 'आंधी तूफान',
        'Light snow': 'हल्की बर्फबारी',
        'Snow': 'बर्फबारी',
        'Heavy snow': 'भारी बर्फबारी',
        'Smoke, haze': 'धुआं और धुंध',
        'Smoke': 'धुआं',
        'Haze': 'धुंध'
    }
    
    if language == 'hinglish':
        # Get Hindi condition or use original
        hindi_condition = condition_hindi.get(condition, condition)
        
        response = f"{location} में अभी तापमान {temp} डिग्री सेल्सियस है। "
        response += f"महसूस हो रहा है {feels} डिग्री। "
        response += f"मौसम {hindi_condition} है। "
        response += f"नमी {humidity} प्रतिशत है और हवा की रफ़्तार {wind} किलोमीटर प्रति घंटा है।"
    else:
        response = f"The temperature in {location} is {temp}°C. "
        response += f"Feels like {feels}°C. "
        response += f"Weather is {condition}. "
        response += f"Humidity is {humidity}% and wind speed is {wind} km/h."
    
    return response

def get_weather_by_city(city, language='english'):
    """Get weather for a specific city"""
    weather_info = get_weather(city)
    return format_weather_response(weather_info, language)

def get_weather_multiple_cities(cities, language='english'):
    """Get weather for multiple cities"""
    if not cities:
        return get_weather_by_city("", language)
    
    responses = []
    for city in cities:
        weather_info = get_weather(city.strip())
        if weather_info:
            temp = weather_info['temperature']
            location = weather_info['location']
            condition_hindi = {
                'Clear': 'साफ़', 'Sunny': 'धूप', 'Mainly clear': 'ज़्यादातर साफ़',
                'Partly cloudy': 'आंशिक बादल', 'Cloudy': 'बादल', 'Overcast': 'घने बादल',
                'Mist': 'धुंध', 'Fog': 'कोहरा', 'Light rain': 'हल्की बारिश',
                'Rain': 'बारिश', 'Heavy rain': 'भारी बारिश', 'Thunderstorm': 'आंधी तूफान',
                'Snow': 'बर्फबारी', 'Smoke, haze': 'धुआं और धुंध'
            }
            
            if language == 'hinglish':
                condition = condition_hindi.get(weather_info['condition'], weather_info['condition'])
                responses.append(f"{location} में {temp} डिग्री और मौसम {condition} है")
            else:
                responses.append(f"{location} is {temp}°C with {weather_info['condition']}")
    
    if not responses:
        if language == 'hinglish':
            return "माफ़ कीजिए, मौसम की जानकारी नहीं मिल पाई।"
        return "Sorry, couldn't fetch weather information."
    
    if language == 'hinglish':
        return "। ".join(responses) + "।"
    return ". ".join(responses) + "."
