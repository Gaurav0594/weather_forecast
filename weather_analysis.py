
import pandas as pd
import requests
from datetime import datetime, timedelta
import json

# Use the same API key from your main.py
API_KEY = "dc722590505687baddb846a381ac120e"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

class WeatherDataAnalyzer:
    def __init__(self):
        self.weather_df = pd.DataFrame() # DataFrame to store weather data
    
    def fetch_weather_data(self, city):
        """Fetch weather data and convert to pandas DataFrame"""
        params = { # parameters
            "q": city,
            "appid": API_KEY,
            "units": "metric" # using metric units like temperature for easier understanding
        }
        
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Convert API data to pandas DataFrame
            weather_list = []
            for item in data['list']:
                weather_record = {
                    'datetime': pd.to_datetime(item['dt'], unit='s'),
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'description': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed'],
                    'city': data['city']['name'],
                    'country': data['city']['country']
                }
                weather_list.append(weather_record)
            
            self.weather_df = pd.DataFrame(weather_list)
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return False
    
    def get_basic_stats(self):
        """Get basic statistical analysis of weather data"""
        if self.weather_df.empty:
            return "No data available"
        
        stats = {
            'Temperature Stats': self.weather_df['temperature'].describe(),
            'Humidity Stats': self.weather_df['humidity'].describe(),
            'Pressure Stats': self.weather_df['pressure'].describe(),
            'Wind Speed Stats': self.weather_df['wind_speed'].describe()
        }
        
        return stats
    
    def get_daily_summary(self):
        """Get daily weather summary using pandas groupby"""
        if self.weather_df.empty:
            return pd.DataFrame()
        
        # Extract date from datetime
        self.weather_df['date'] = self.weather_df['datetime'].dt.date
        
        daily_summary = self.weather_df.groupby('date').agg({ # groupby combine each group
            'temperature': ['min', 'max', 'mean'],
            'humidity': 'mean',
            'pressure': 'mean',
            'wind_speed': 'mean'
        }).round(2)
        
        return daily_summary
    
    def find_extreme_conditions(self):
        """Find extreme weather conditions"""
        if self.weather_df.empty: 
            return {}
        
        extremes = {
            'Hottest': self.weather_df.loc[self.weather_df['temperature'].idxmax()],
            'Coldest': self.weather_df.loc[self.weather_df['temperature'].idxmin()],
            'Most Humid': self.weather_df.loc[self.weather_df['humidity'].idxmax()],
            'Windiest': self.weather_df.loc[self.weather_df['wind_speed'].idxmax()]
        }
        
        return extremes
    
    def get_weather_trends(self):
        """Analyze weather trends over time"""
        if self.weather_df.empty:
            return {}
        
        # Sort by datetime
        df_sorted = self.weather_df.sort_values('datetime')
        
        trends = {
            'Temperature Trend': 'Increasing' if df_sorted['temperature'].iloc[-1] > df_sorted['temperature'].iloc[0] else 'Decreasing',
            'Humidity Trend': 'Increasing' if df_sorted['humidity'].iloc[-1] > df_sorted['humidity'].iloc[0] else 'Decreasing',
            'Pressure Trend': 'Increasing' if df_sorted['pressure'].iloc[-1] > df_sorted['pressure'].iloc[0] else 'Decreasing'
        }
        
        return trends
    
    def export_to_csv(self, filename=None):
        """Export weather data to CSV file"""
        if self.weather_df.empty:
            print("No data to export")
            return False
        
        if filename is None:
            city = self.weather_df['city'].iloc[0]
            filename = f"weather_data_{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        self.weather_df.to_csv(filename, index=False) # create a CSV file with given name
        print(f"Data exported to {filename}")
        return True
    
    def display_formatted_forecast(self):
        """Display weather forecast in a formatted table"""
        if self.weather_df.empty:
            return "No data available"
        
        # Select relevant columns for display
        display_df = self.weather_df[['datetime', 'temperature', 'description', 'humidity', 'wind_speed']].copy()
        display_df['datetime'] = display_df['datetime'].dt.strftime('%Y-%m-%d %H:%M')
        
        return display_df.to_string(index=False) # false are used to index does't carry

def main():
    """Main function to demonstrate weather analysis"""
    analyzer = WeatherDataAnalyzer()
    
    # Get city from user
    city = input("Enter city name for weather analysis: ").strip()
    if not city:
        city = "Meerut"  # Default city
    
    print(f"\nFetching weather data for {city}...")
    
    if analyzer.fetch_weather_data(city):
        print("✓ Data fetched successfully!\n")
        
        # Display formatted forecast
        print("=== WEATHER FORECAST ===")
        print(analyzer.display_formatted_forecast())
        print("\n")
        
        # Show basic statistics
        print("=== STATISTICAL ANALYSIS ===")
        stats = analyzer.get_basic_stats()
        for stat_name, stat_data in stats.items():
            print(f"\n{stat_name}:")
            print(stat_data)
        
        # Show daily summary
        print("\n=== DAILY SUMMARY ===")
        daily_summary = analyzer.get_daily_summary()
        if not daily_summary.empty:
            print(daily_summary)
        
        # Show extreme conditions
        print("\n=== EXTREME CONDITIONS ===")
        extremes = analyzer.find_extreme_conditions()
        for condition, data in extremes.items():
            print(f"{condition}: {data['temperature']}°C at {data['datetime']}")
        
        # Show trends
        print("\n=== WEATHER TRENDS ===")
        trends = analyzer.get_weather_trends()
        for trend_name, trend_value in trends.items():
            print(f"{trend_name}: {trend_value}")
        
        # Export option
        export = input("\nExport data to CSV? (yes/no): ").strip().lower()
        if export == 'yes':
            analyzer.export_to_csv()
    
    else:
        print("✗ Failed to fetch weather data")

if __name__ == "__main__":
    main()
