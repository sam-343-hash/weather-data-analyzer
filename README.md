# 🌦️ Weather Data Analyzer

A beginner-friendly Python project that fetches **real weather data** from a free API, analyzes trends, and generates beautiful charts — no API key needed!

---

## 📸 Sample Output

```
═══════════════════════════════════════════════════════
  🌦️  Data Analyzer  |  Powered by Open-Meteo
═══════════════════════════════════════════════════════

Enter city name (e.g. Mumbai, London, New York): Delhi
How many days to analyze? (default 7, max 14): 7

📡 Fetching weather data for 'Delhi'...
📍 Location resolved: Delhi, Delhi, India (28.66°, 77.23°)
✅ Got 7 days of weather data!

──────────────────────────────────────────────
  📊 WEATHER SUMMARY — Delhi, Delhi, India
  📅 Last 7 days
──────────────────────────────────────────────
  🌡️  Avg Temperature  : 36.4 °C
  🔺  Hottest Day      : 42.1 °C  (Wednesday, May 08)
  🔻  Coldest Day      : 29.3 °C  (Monday, May 06)
  🌧️  Total Rain        : 0.0 mm
  🌂  Rainy Days       : 0 days
  💨  Avg Wind Speed   : 18.7 km/h
──────────────────────────────────────────────

📊 Generating charts...
✅ Chart saved to 'charts/weather_analysis.png'
💾 Data saved to 'data/delhi_weather.csv'

🎉 Analysis complete! Check the 'charts/' and 'data/' folders.
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/weather-data-analyzer.git
cd weather-data-analyzer
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the analyzer
```bash
python weather_analyzer.py
```

---

## 📁 Project Structure

```
weather-data-analyzer/
│
├── weather_analyzer.py     # 🏠 Main script — run this!
├── requirements.txt        # 📦 Python dependencies
├── .gitignore              # 🙈 Files to ignore in Git
├── README.md               # 📖 You're reading this
│
├── utils/
│   ├── __init__.py
│   └── helpers.py          # 🛠️ Helper functions (geocoding, formatting)
│
├── charts/                 # 📊 Generated chart images (auto-created)
│   └── weather_analysis.png
│
└── data/                   # 💾 Saved CSV files (auto-created)
    └── <city>_weather.csv
```

---

## 📊 What It Analyzes

| Feature | Description |
|---|---|
| 🌡️ Temperature | Daily max, min, and average over selected days |
| 🌧️ Precipitation | Daily rainfall in mm, rainy day count |
| 💨 Wind Speed | Max wind speed per day |
| 📈 Charts | Beautiful dark-themed multi-panel chart |
| 💾 CSV Export | Raw data saved for further analysis |

---

## 🔧 Technologies Used

| Library | Purpose |
|---|---|
| `requests` | Fetch data from the Open-Meteo API |
| `pandas` | Data cleaning and analysis |
| `matplotlib` | Chart generation |

---

## 🌐 API Used

This project uses **[Open-Meteo](https://open-meteo.com/)** — a completely **free, no-API-key-needed** weather API.

- Geocoding API: Converts city names → coordinates
- Forecast API: Returns historical + forecast weather data

---

## 💡 Ideas to Extend This Project

- [ ] Add a comparison mode (city vs city)
- [ ] Export charts as PDF report
- [ ] Add a web interface using Flask
- [ ] Send a daily weather summary email
- [ ] Predict tomorrow's temp using linear regression

---

## 📄 License

MIT License — feel free to use and modify!

---

> Made with ❤️ and Python 🐍
