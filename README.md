# Stock Price Tracker

A Stock Price Tracker Web App built with Python and Streamlit. It fetches real stock price data from Yahoo Finance, stores it in a local SQLite database, analyzes trends and returns, and displays everything in a browser with interactive charts.

---

## What This Project Does

1. **Fetches** real stock price data from the internet
2. **Stores** that data in a local database on your laptop
3. **Analyzes** the data — calculates trends, returns, averages
4. **Shows** everything in a web browser with interactive charts

---

## Tech Stack

### 1. Python
- The main programming language
- Everything is written in Python
- All other tools are Python libraries

### 2. yfinance
- Fetches stock data from Yahoo Finance
- Free, no API key needed, very simple to use
- Gives us: Date, Open, High, Low, Close price, Volume for any stock

```python
yf.download("AAPL", period="6mo")  # gives 6 months of Apple stock data
```

### 3. Pandas
- Works with data in tables (like Excel in code)
- Used to clean, filter, sort, and calculate on stock data
- Stores stock data in a DataFrame
- Calculates moving averages, filters by ticker, exports to SQLite

### 4. NumPy
- Python library for mathematical calculations
- Used behind the scenes in calculations like % return and averages

### 5. SQLite (via sqlite3)
- Lightweight database that lives as a single file on your laptop
- Stores stock data so we don't fetch it every time
- One table: `stock_prices` — stores ticker, date, open, high, low, close, volume
- File location: `stock-tracker/data/stocks.db`

### 6. Matplotlib
- Python's classic chart drawing library
- Used to generate and save charts as PNG image files
- Draws line charts and bar charts, saves them to the `/charts` folder
- Used by `main.py` (the non-web version)

### 7. Plotly
- Interactive charting library
- Charts are interactive — zoom, hover, click
- Powers all charts inside the Streamlit web app
- Hover over a chart to see exact price on any date

### 8. Streamlit
- Turns Python code into a web app
- No HTML, CSS, or JavaScript needed — just Python
- Creates the sidebar with dropdowns and buttons
- Shows summary metric cards and Plotly charts in tabs
- Runs a local web server at `http://localhost:8501`

---

## Project Structure

```
stock-tracker/
│
├── app.py              ← Streamlit web app (the UI)
├── main.py             ← Run without web (terminal only)
├── config.py           ← Settings: which stocks, time period, MA days
├── requirements.txt    ← List of all libraries to install
│
├── src/
│   ├── fetch_data.py   ← Uses yfinance to download stock data
│   ├── store_data.py   ← Saves/loads data from SQLite database
│   ├── analyze.py      ← Calculates MA, daily return, volatility, stats
│   └── visualize.py    ← Draws charts using matplotlib (for main.py)
│
├── data/
│   └── stocks.db       ← SQLite database file (auto created)
│
└── charts/             ← PNG chart images (auto created by main.py)
```

---

## How Data Flows Through the Project

```
Yahoo Finance
     ↓
  yfinance          ← fetch_data.py downloads the data
     ↓
  pandas            ← cleans and structures it as a table
     ↓
  SQLite            ← store_data.py saves it to the database
     ↓
  pandas            ← analyze.py loads it back and calculates indicators
     ↓
  Plotly            ← draws interactive charts
     ↓
  Streamlit         ← displays everything in the browser
```

---

## What Each File Does

| File | Job |
|---|---|
| `config.py` | Central settings — change stocks or period here |
| `fetch_data.py` | Goes to Yahoo Finance, downloads stock prices |
| `store_data.py` | Saves data to database, loads it back when needed |
| `analyze.py` | Calculates moving averages, daily return, % gain/loss |
| `visualize.py` | Draws and saves charts as PNG (used by main.py) |
| `app.py` | The web app — sidebar, tabs, charts, summary cards |
| `main.py` | Terminal version — fetch, save, analyze, save charts |

---

## What the Web App Shows

| Section | What You See |
|---|---|
| Summary cards | Current price and total % return for each stock |
| Tab 1 | Line chart — price over time with moving averages |
| Tab 2 | Bar chart — how much the stock was traded each day |
| Tab 3 | Green/red bars — daily % gain or loss |
| Tab 4 | All stocks on one chart (normalized) + return table |

---

## Key Concepts

**Moving Average** — smooths out price noise. 7-day MA = average of last 7 days closing prices. Helps see the trend.

**Daily Return** — how much % the stock went up or down each day.

**Normalized Comparison** — to compare stocks fairly, start price is set to 100 for all. Then you see who grew more, not who costs more.

**Volatility** — how much the price swings day to day. High volatility = risky stock.

---

## Installation

```bash
pip install -r requirements.txt
```

---

## How to Run

### Web App (Streamlit)
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

### Terminal Version
```bash
python main.py
```
Fetches data, saves to DB, and saves charts to `/charts` folder.

---

## First Time Setup

1. Run the app: `streamlit run app.py`
2. Select stocks from the left sidebar
3. Click **Fetch Latest Data** button
4. Charts will appear

---

## Configuration

Edit `config.py` to change default settings:

```python
STOCKS = ["MDTA", "TCS", "GOOGL", "MSFT", "AMZN"]  # stocks to track
PERIOD = "6mo"                                         # data period
SHORT_MA = 7                                           # short moving average days
LONG_MA = 30                                           # long moving average days
```

---

## To Stop the App

Press `Ctrl + C` in the terminal.
