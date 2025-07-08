# Custom_Weather_Map_Tool.py

import os
import requests
import folium
from typing import Any, Dict
from datetime import datetime
from pydantic import Field, PrivateAttr
from agentpro.tools import Tool
import streamlit as st
from streamlit_folium import folium_static


class WeatherMapTool_OpenWeather(Tool):
    name: str = Field(default="Weather Map Tool (Free)")
    description: str = Field(default="Shows current weather and forecast with a map using OpenWeatherMap free API.")
    action_type: str = Field(default="weather_map")
    input_format: str = Field(default="City name as a string.")

    _config: Dict[str, Any] = PrivateAttr()

    def __init__(self, api_key: str = None, **kwargs):
        super().__init__(**kwargs)
        self._config = {
            "api_key": api_key or os.getenv("OPENWEATHER_API_KEY")
        }

    def run(self, input_text: Any) -> str:
        city = input_text.strip()

        # Current weather endpoint (free tier)
        current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={self._config['api_key']}"
        current_resp = requests.get(current_url).json()

        if current_resp.get("cod") != 200:
            return f"❌ Failed to get weather for {city}. Error: {current_resp.get('message')}"

        lat = current_resp["coord"]["lat"]
        lon = current_resp["coord"]["lon"]

        # Forecast (5-day / 3-hour interval)
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={self._config['api_key']}"
        forecast_resp = requests.get(forecast_url).json()
        if forecast_resp.get("cod") != "200":
            return f"❌ Failed to get forecast for {city}. Error: {forecast_resp.get('message')}"

        # 🟢 CURRENT WEATHER
        weather = current_resp["weather"][0]
        current_block = f"""
        ### 🌤️ Current Weather in {city}
        - 🌡️ Temperature: **{current_resp['main']['temp']}°C**
        - 🌬️ Wind: {current_resp['wind']['speed']} m/s
        - 💧 Humidity: {current_resp['main']['humidity']}%
        - 📈 Pressure: {current_resp['main']['pressure']} hPa
        - 🌥️ Condition: {weather['main']} - {weather['description'].title()}
        """

        # 📅 FORECAST
        forecast_block = "### 📅 Forecast (Next 5 Days):\n"
        seen_days = set()
        for entry in forecast_resp["list"]:
            date = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S")
            day = date.strftime("%A %d %b, %H:%M")
            temp = entry["main"]["temp"]
            cond = entry["weather"][0]["description"]
            if date.date() not in seen_days and date.hour == 12:
                forecast_block += f"- **{day}**: {cond.title()}, 🌡️ {temp}°C\n"
                seen_days.add(date.date())

        # 🌍 MAP
        m = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker([lat, lon], tooltip=f"{city}: {current_resp['main']['temp']}°C").add_to(m)
        folium_static(m)

        # Store display elements in session state for persistence
        st.session_state["weather_output"] = {
            "current_block": current_block,
            "forecast_block": forecast_block,
            "map_location": (lat, lon),
            "temp": current_resp["main"]["temp"],
            "city": city
        }

        # 🧠 AGENT SUMMARY RETURN (so the agent can reason)
        final_summary = f"""
✅ Final Answer
Here is the current weather and forecast for **{city}**:

{current_block}

{forecast_block}

➡️ The above information is also available visually via the map. The agent can now use this structured result to analyze trends, answer follow-up queries, or make suggestions.
"""

        st.markdown(current_block)
        st.markdown(forecast_block)

        return final_summary


