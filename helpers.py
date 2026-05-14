"""
🛠️ Helper utilities for the Weather Data Analyzer
"""

import requests


# WMO Weather Code descriptions
WEATHER_CODES = {
    0: "☀️ Clear sky",
    1: "🌤️ Mainly clear",
    2: "⛅ Partly cloudy",
    3: "☁️ Overcast",
    45: "🌫️ Foggy",
    48: "🌫️ Icy fog",
    51: "🌦️ Light drizzle",
    53: "🌦️ Moderate drizzle",
    55: "🌧️ Dense drizzle",
    61: "🌧️ Slight rain",
    63: "🌧️ Moderate rain",
    65: "🌧️ Heavy rain",
    71: "❄️ Slight snow",
    73: "❄️ Moderate snow",
    75: "❄️ Heavy snow",
    80: "🌦️ Slight showers",
    81: "🌧️ Moderate showers",
    82: "⛈️ Violent showers",
    95: "⛈️ Thunderstorm",
    99: "⛈️ Thunderstorm w/ hail",
}


def get_coordinates(city: str) -> tuple[float, float, str]:
    """
    Get latitude/longitude for a city using the Open-Meteo Geocoding API.
    Returns (lat, lon, resolved_city_name)
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "en", "format": "json"}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if not data.get("results"):
        raise ValueError(f"❌ City '{city}' not found. Please check the spelling and try again.")

    result = data["results"][0]
    name = result["name"]
    country = result.get("country", "")
    state = result.get("admin1", "")

    if state and state != name:
        resolved = f"{name}, {state}, {country}"
    else:
        resolved = f"{name}, {country}"

    return result["latitude"], result["longitude"], resolved


def describe_weather_code(code: int) -> str:
    """Return a human-readable description for a WMO weather code."""
    return WEATHER_CODES.get(code, "🌡️ Unknown")


def print_banner():
    """Print a stylish ASCII banner."""
    print("\n" + "=" * 55)
    print("""
  ██╗    ██╗███████╗ █████╗ ████████╗██╗  ██╗███████╗██████╗ 
  ██║    ██║██╔════╝██╔══██╗╚══██╔══╝██║  ██║██╔════╝██╔══██╗
  ██║ █╗ ██║█████╗  ███████║   ██║   ███████║█████╗  ██████╔╝
  ██║███╗██║██╔══╝  ██╔══██║   ██║   ██╔══██║██╔══╝  ██╔══██╗
  ╚███╔███╔╝███████╗██║  ██║   ██║   ██║  ██║███████╗██║  ██║
   ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
          🌦️  Data Analyzer  |  Powered by Open-Meteo
    """)
    print("=" * 55)


def print_summary(city: str, stats: dict, days: int):
    """Print a formatted summary of weather statistics."""
    print("\n" + "─" * 45)
    print(f"  📊 WEATHER SUMMARY — {city}")
    print(f"  📅 Last {days} days")
    print("─" * 45)
    print(f"  🌡️  Avg Temperature  : {stats['avg_temp']:.1f} °C")
    print(f"  🔺  Hottest Day      : {stats['max_temp']:.1f} °C  ({stats['hottest_day']})")
    print(f"  🔻  Coldest Day      : {stats['min_temp']:.1f} °C  ({stats['coldest_day']})")
    print(f"  🌧️  Total Rain        : {stats['total_precipitation']:.1f} mm")
    print(f"  🌂  Rainy Days       : {stats['rainy_days']} days")
    print(f"  💨  Avg Wind Speed   : {stats['avg_wind']:.1f} km/h")
    print(f"  🌊  Rainiest Day     : {stats['rainiest_day']}")
    print("─" * 45 + "\n")
