
import streamlit as st
import pandas as pd
from weather_analysis import WeatherDataAnalyzer
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Weather Forecast Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Main Application ---

# 1. Header Section
st.image('assets/banner.png', use_container_width=True)
st.title("Weather Forecast Dashboard")
st.markdown("An interactive dashboard to get real-time weather forecasts for any city.")

# --- Sidebar for User Input ---
st.sidebar.header("Configuration")

# Default cities list
default_cities = ["Meerut", "Delhi", "Alwar", "Noida", "Gurgaon"]

# Select box for default cities
selected_city = st.sidebar.selectbox("Choose a default city:", default_cities)

# Text input for custom city
custom_city = st.sidebar.text_input("Enter a city name:")

# Determine the city to use
city = custom_city if custom_city else selected_city

if st.sidebar.button("Get Weather Data", type="primary"):
    analyzer = WeatherDataAnalyzer()
    if analyzer.fetch_weather_data(city):
        st.session_state['weather_df'] = analyzer.weather_df
        st.session_state['city'] = city
        st.sidebar.success(f"Successfully fetched data for {city}.")
    else:
        st.sidebar.error(f"Could not fetch weather data for {city}.")
        st.session_state.clear()

st.sidebar.info(
    "Choose a default city or enter a custom city name and click the button to view the forecast, statistics, and extreme conditions."
)

# --- Main Content ---
if 'weather_df' in st.session_state:
    df = st.session_state['weather_df']
    city = st.session_state['city']
    
    # 2. Key Metrics Section
    st.header(f"Current & Upcoming Conditions in {city}")
    
    # Get the first row for "current" metrics
    current = df.iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌡️ Temperature", f"{current['temperature']:.2f}°C", help="Current temperature.")
    col2.metric("💧 Humidity", f"{current['humidity']}%", help="Current humidity level.")
    col3.metric("💨 Wind Speed", f"{current['wind_speed']:.2f} m/s", help="Current wind speed.")
    col4.metric("📝 Description", current['description'].title(), help="Current weather description.")

    # 3. Data Visualization Section
    st.header("Data Visualizations")
    
    tab1, tab2 = st.tabs(["Temperature & Humidity", "Wind Speed Analysis"])
    
    with tab1:
        st.subheader("Temperature and Humidity Over Time")
        st.line_chart(df.rename(columns={'datetime':'index'}).set_index('index')[['temperature', 'humidity']], use_container_width=True)
    
    with tab2:
        st.subheader("Wind Speed Over Time")
        st.bar_chart(df.rename(columns={'datetime':'index'}).set_index('index')['wind_speed'], use_container_width=True)

    # 4. Detailed Forecast Table
    st.header("5-Day Weather Forecast")
    forecast_df = df[['datetime', 'temperature', 'description', 'wind_speed', 'humidity', 'pressure']]
    st.dataframe(forecast_df.style.format({
        "temperature": "{:.2f}°C",
        "wind_speed": "{:.2f} m/s",
        "humidity": "{}%",
        "pressure": "{} hPa"
    }).highlight_max(subset=['temperature'], color='lightcoral').highlight_min(subset=['temperature'], color='lightblue'))

    # 5. Extreme Conditions Section
    st.header("Extreme Weather Conditions")
    analyzer = WeatherDataAnalyzer()
    analyzer.weather_df = df
    extremes = analyzer.find_extreme_conditions()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info(f"**Hottest 🔥**\n\n{extremes['Hottest']['temperature']:.2f}°C")
    with col2:
        st.info(f"**Coldest ❄️**\n\n{extremes['Coldest']['temperature']:.2f}°C")
    with col3:
        st.info(f"**Most Humid 💧**\n\n{extremes['Most Humid']['humidity']}%")
    with col4:
        st.info(f"**Windiest 🌬️**\n\n{extremes['Windiest']['wind_speed']:.2f} m/s")

    # 6. Download Button
    st.header("Download Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'weather_data_{city}_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
        help="Download the raw forecast data in CSV format."
    )
