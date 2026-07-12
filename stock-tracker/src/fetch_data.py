import yfinance as yf
import pandas as pd
import requests
import sys
import os
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["PYTHONHTTPSVERIFY"] = "0"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import STOCKS, PERIOD


def fetch_stock(ticker: str, period: str = PERIOD) -> pd.DataFrame:
    print(f"  Fetching {ticker}...")
    try:
        df = yf.download(
            ticker,
            period=period,
            auto_adjust=True,
            progress=False,
        )
    except Exception as e:
        print(f"  Error fetching {ticker}: {e}")
        return pd.DataFrame()

    if df.empty:
        print(f"  Warning: No data returned for {ticker}")
        return pd.DataFrame()

    # yf.download returns MultiIndex columns when multi=True, flatten them
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()
    df["Ticker"] = ticker
    df = df.rename(columns={"Price": "Date"}) if "Price" in df.columns else df
    df = df[["Ticker", "Date", "Open", "High", "Low", "Close", "Volume"]]
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df


def fetch_all_stocks(tickers: list = STOCKS, period: str = PERIOD) -> pd.DataFrame:
    all_data = []
    for i, ticker in enumerate(tickers):
        df = fetch_stock(ticker, period)
        if not df.empty:
            all_data.append(df)
        if i < len(tickers) - 1:
            time.sleep(1)

    if not all_data:
        print("No data fetched.")
        return pd.DataFrame()

    combined = pd.concat(all_data, ignore_index=True)
    print(f"  Fetched {len(combined)} total rows for {len(all_data)} stocks.")
    return combined
