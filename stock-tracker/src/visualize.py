import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHORT_MA, LONG_MA, CHARTS_DIR


def _save(fig, filename: str):
    os.makedirs(CHARTS_DIR, exist_ok=True)
    path = os.path.join(CHARTS_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  Chart saved: {path}")


def plot_price_and_ma(df: pd.DataFrame, ticker: str):
    dates = pd.to_datetime(df["date"])

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(dates, df["close"], label="Close Price", color="#1f77b4", linewidth=1.5)
    ax.plot(dates, df[f"MA{SHORT_MA}"], label=f"{SHORT_MA}-day MA", color="#ff7f0e", linewidth=1.2, linestyle="--")
    ax.plot(dates, df[f"MA{LONG_MA}"], label=f"{LONG_MA}-day MA", color="#2ca02c", linewidth=1.2, linestyle="--")

    ax.set_title(f"{ticker} — Close Price & Moving Averages", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()
    ax.grid(alpha=0.3)

    _save(fig, f"{ticker}_price_ma.png")


def plot_volume(df: pd.DataFrame, ticker: str):
    dates = pd.to_datetime(df["date"])

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.bar(dates, df["volume"], color="#1f77b4", alpha=0.6, width=1)
    ax.set_title(f"{ticker} — Trading Volume", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()
    ax.grid(alpha=0.3, axis="y")

    _save(fig, f"{ticker}_volume.png")


def plot_daily_return(df: pd.DataFrame, ticker: str):
    dates = pd.to_datetime(df["date"])
    returns = df["daily_return"].fillna(0)

    colors = ["#2ca02c" if r >= 0 else "#d62728" for r in returns]

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.bar(dates, returns, color=colors, width=1, alpha=0.8)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title(f"{ticker} — Daily Return (%)", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Return (%)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()
    ax.grid(alpha=0.3, axis="y")

    _save(fig, f"{ticker}_daily_return.png")


def plot_comparison(all_data: dict):
    fig, ax = plt.subplots(figsize=(12, 5))

    for ticker, df in all_data.items():
        dates = pd.to_datetime(df["date"])
        normalized = (df["close"] / df["close"].iloc[0]) * 100
        ax.plot(dates, normalized, label=ticker, linewidth=1.5)

    ax.set_title("Stock Comparison — Normalized Price (Base = 100)", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Price")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()
    ax.grid(alpha=0.3)

    _save(fig, "all_stocks_comparison.png")


def plot_all_for_ticker(df: pd.DataFrame, ticker: str):
    print(f"\n  Generating charts for {ticker}...")
    plot_price_and_ma(df, ticker)
    plot_volume(df, ticker)
    plot_daily_return(df, ticker)
