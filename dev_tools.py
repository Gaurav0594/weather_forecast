
import sys
import os
import subprocess
from weather_analysis import WeatherDataAnalyzer

def show_help():
    print("""
Available Commands:
  run             - Run the main weather application.
  analyze         - Run the basic weather analysis script.
  full-analysis   - Run a full weather analysis for a specified city.
  test            - Run project tests.
  check           - Check environment setup.
  help            - Show this help message.
    """)

def run_app():
    print("Running main application...")
    subprocess.run([sys.executable, "main.py"])

def run_weather_analysis():
    print("Running weather analysis script...")
    subprocess.run([sys.executable, "weather_analysis.py"])

def run_full_analysis():
    """Runs a comprehensive weather analysis for a given city."""
    if len(sys.argv) < 3:
        print("Error: City name is required for full-analysis.")
        print("Usage: python dev_tools.py full-analysis <CityName>")
        return

    city = sys.argv[2]
    print(f"--- Starting Full Weather Analysis for {city} ---")
    
    analyzer = WeatherDataAnalyzer()
    
    if not analyzer.fetch_weather_data(city):
        print(f"✗ Failed to fetch weather data for {city}.")
        return

    print(f"\n✓ Weather data fetched successfully for {city}.")

    # 1. Display Forecast
    print("\n" + "="*20 + " 5-Day Forecast " + "="*20)
    print(analyzer.display_formatted_forecast())
    
    # 2. Display Statistics
    print("\n" + "="*20 + " Statistical Summary " + "="*18)
    stats = analyzer.get_basic_stats()
    for title, data in stats.items():
        print(f"\n--- {title} ---")
        print(data.to_string())

    # 3. Display Extreme Conditions
    print("\n" + "="*20 + " Extreme Conditions " + "="*19)
    extremes = analyzer.find_extreme_conditions()
    for condition, data in extremes.items():
        print(f"\n{condition}:")
        print(f"  Date/Time:   {data['datetime'].strftime('%Y-%m-%d %H:%M')}")
        print(f"  Temperature: {data['temperature']}°C")
        print(f"  Humidity:    {data['humidity']}%")
        print(f"  Wind Speed:  {data['wind_speed']} m/s")
        print(f"  Description: {data['description']}")

    print("\n--- Analysis Complete ---")

def run_tests():
    """Run tests (placeholder)"""
    print("Running tests...")

def check_env():
    """Check environment (placeholder)"""
    print("Checking environment...")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
    else:
        command = sys.argv[1].lower()
        if command == "test":
            run_tests()
        elif command == "check":
            check_env()
        elif command == "run":
            run_app()
        elif command == "analyze":
            run_weather_analysis()
        elif command == "full-analysis":
            run_full_analysis()
        elif command == "help":
            show_help()
        else:
            print(f"Unknown command: {command}")
            show_help()
