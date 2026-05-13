"""
🌦️ Weather Data Analyzer
Fetches real weather data from Open-Meteo API and analyzes trends.
No API key needed — completely free!
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from utils.helpers import get_coordinates, print_banner, print_summary


def fetch_weather_data(city: str, days: int = 7) -> dict:
    """Fetch historical + forecast weather data from Open-Meteo API."""
    print(f"\n📡 Fetching weather data for '{city}'...")

    lat, lon, resolved_city = get_coordinates(city)
    print(f"📍 Location resolved: {resolved_city} ({lat:.2f}°, {lon:.2f}°)")

    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "windspeed_10m_max",
            "weathercode",
        ],
        "timezone": "auto",
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    print(f"✅ Got {len(data['daily']['time'])} days of weather data!\n")
    return data, resolved_city


def parse_to_dataframe(raw_data: dict) -> pd.DataFrame:
    """Convert raw API response into a clean pandas DataFrame."""
    daily = raw_data["daily"]
    df = pd.DataFrame({
        "date": pd.to_datetime(daily["time"]),
        "temp_max": daily["temperature_2m_max"],
        "temp_min": daily["temperature_2m_min"],
        "temp_avg": [(mx + mn) / 2 for mx, mn in zip(daily["temperature_2m_max"], daily["temperature_2m_min"])],
        "precipitation": daily["precipitation_sum"],
        "wind_speed": daily["windspeed_10m_max"],
        "weather_code": daily["weathercode"],
    })
    return df


def analyze(df: pd.DataFrame) -> dict:
    """Run basic statistical analysis on the weather data."""
    stats = {
        "avg_temp": df["temp_avg"].mean(),
        "max_temp": df["temp_max"].max(),
        "min_temp": df["temp_min"].min(),
        "total_precipitation": df["precipitation"].sum(),
        "avg_wind": df["wind_speed"].mean(),
        "hottest_day": df.loc[df["temp_max"].idxmax(), "date"].strftime("%A, %b %d"),
        "coldest_day": df.loc[df["temp_min"].idxmin(), "date"].strftime("%A, %b %d"),
        "rainiest_day": df.loc[df["precipitation"].idxmax(), "date"].strftime("%A, %b %d"),
        "rainy_days": (df["precipitation"] > 1).sum(),
    }
    return stats


def generate_charts(df: pd.DataFrame, city: str):
    """Generate and save weather analysis charts."""
    print("📊 Generating charts...")
    fig, axes = plt.subplots(3, 1, figsize=(12, 14))
    fig.suptitle(f"🌦️ Weather Analysis — {city}", fontsize=18, fontweight="bold", y=0.98)
    fig.patch.set_facecolor("#0f1117")

    for ax in axes:
        ax.set_facecolor("#1a1d2e")
        ax.tick_params(colors="#aab4be")
        ax.spines[:].set_color("#2e3347")

    # --- Chart 1: Temperature Range ---
    ax1 = axes[0]
    ax1.fill_between(df["date"], df["temp_min"], df["temp_max"], alpha=0.3, color="#4fc3f7", label="Temp Range")
    ax1.plot(df["date"], df["temp_max"], "o-", color="#ff7043", linewidth=2, markersize=5, label="Max Temp °C")
    ax1.plot(df["date"], df["temp_min"], "o-", color="#4fc3f7", linewidth=2, markersize=5, label="Min Temp °C")
    ax1.plot(df["date"], df["temp_avg"], "--", color="#ffca28", linewidth=1.5, label="Avg Temp °C")
    ax1.set_title("🌡️ Temperature Trends", color="white", fontsize=13, pad=10)
    ax1.set_ylabel("Temperature (°C)", color="#aab4be")
    ax1.legend(facecolor="#1a1d2e", labelcolor="white", edgecolor="#2e3347")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

    # --- Chart 2: Precipitation ---
    ax2 = axes[1]
    colors = ["#2979ff" if p > 5 else "#64b5f6" if p > 1 else "#b0bec5" for p in df["precipitation"]]
    bars = ax2.bar(df["date"], df["precipitation"], color=colors, width=0.6, edgecolor="#0f1117")
    ax2.set_title("🌧️ Daily Precipitation", color="white", fontsize=13, pad=10)
    ax2.set_ylabel("Precipitation (mm)", color="#aab4be")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    # Add value labels on bars
    for bar, val in zip(bars, df["precipitation"]):
        if val > 0.5:
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                     f"{val:.1f}", ha="center", va="bottom", color="white", fontsize=8)

    # --- Chart 3: Wind Speed ---
    ax3 = axes[2]
    ax3.plot(df["date"], df["wind_speed"], "o-", color="#ab47bc", linewidth=2, markersize=6)
    ax3.fill_between(df["date"], df["wind_speed"], alpha=0.2, color="#ab47bc")
    ax3.set_title("💨 Wind Speed", color="white", fontsize=13, pad=10)
    ax3.set_ylabel("Wind Speed (km/h)", color="#aab4be")
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    output_path = "charts/weather_analysis.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"✅ Chart saved to '{output_path}'\n")


def save_to_csv(df: pd.DataFrame, city: str):
    """Save the cleaned weather data to CSV."""
    filename = f"data/{city.lower().replace(' ', '_')}_weather.csv"
    df.to_csv(filename, index=False)
    print(f"💾 Data saved to '{filename}'")


def main():
    print_banner()

    city = input("Enter city name (e.g. Mumbai, London, New York): ").strip()
    if not city:
        city = "Mumbai"

    try:
        days_input = input("How many days to analyze? (default 7, max 14): ").strip()
        days = int(days_input) if days_input.isdigit() else 7
        days = min(max(days, 1), 14)
    except ValueError:
        days = 7

    raw_data, resolved_city = fetch_weather_data(city, days)
    df = parse_to_dataframe(raw_data)
    stats = analyze(df)

    print_summary(resolved_city, stats, days)
    generate_charts(df, resolved_city)
    save_to_csv(df, resolved_city)

    print("\n🎉 Analysis complete! Check the 'charts/' and 'data/' folders.\n")


if __name__ == "__main__":
    main()
