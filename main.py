import requests
from datetime import datetime

API_KEY = "dc722590505687baddb846a381ac120e"  # Replace with your OpenWeather API key
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

def get_location():
    """Get user's approximate location (lat, lon, city, country) via IP"""
    try:
        res = requests.get("http://ip-api.com/json/")
        data = res.json()
        if data['status'] == 'success':
            return data['lat'], data['lon'], data['city'], data['country']
        else:
            return None
    except Exception as e:
        print("Error fetching location:", e)
        return None


def get_weather_forecast_by_city(city):
    """Fetch forecast using city name"""
    params = { # using paramerters
        "q": city,
        "appid": API_KEY,
        "units": "metric" # Using metric units like temperature for easier understanding
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return parse_forecast(data)
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch weather data. {str(e)}"


def get_weather_forecast_by_coords(lat, lon):
    """Fetch forecast using latitude and longitude"""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params) # Fetching data for given coordinates use try requests
        response.raise_for_status()
        data = response.json()
        return parse_forecast(data)
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch weather data. {str(e)}"


def parse_forecast(data):
    try:
        city = data['city']['name']
        country = data['city']['country']
        forecast = []
        for item in data['list'][:5]:  # Next 5 slots
            date = datetime.fromtimestamp(item['dt'])
            temp = item['main']['temp']
            description = item['weather'][0]['description']
            forecast.append(f"{date.strftime('%Y-%m-%d %H:%M')}: {temp}°C, {description}")
        return f"Weather forecast for {city}, {country}:\n" + "\n".join(forecast)
    except KeyError as e:
        return f"Error: Missing key in API response. {str(e)}"


def main():
    # User choice
    choice = input("Press ENTER for auto location or type a city name: ").strip()

    if choice:  # User entered a city
        result = get_weather_forecast_by_city(choice)
        print(result)
    else:  # Auto detect location
        location = get_location()
        if location:
            lat, lon, city, country = location
            print(f"Detected Location: {city}, {country} ({lat},{lon})")
            result = get_weather_forecast_by_coords(lat, lon)
            print(result)
        else:
            print("Could not detect location.")


if __name__ == "__main__":
    main()
