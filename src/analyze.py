import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHORT_MA, LONG_MA


def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df[f"MA{SHORT_MA}"] = df["close"].rolling(window=SHORT_MA).mean()
    df[f"MA{LONG_MA}"] = df["close"].rolling(window=LONG_MA).mean()
    return df


def add_daily_return(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["daily_return"] = df["close"].pct_change() * 100
    return df


def add_volatility(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    df = df.copy()
    df["volatility"] = df["daily_return"].rolling(window=window).std()
    return df


def summary_stats(df: pd.DataFrame) -> dict:
    return {
        "ticker": df["ticker"].iloc[0],
        "start_date": df["date"].min(),
        "end_date": df["date"].max(),
        "total_days": len(df),
        "start_price": round(df["close"].iloc[0], 2),
        "end_price": round(df["close"].iloc[-1], 2),
        "highest_price": round(df["high"].max(), 2),
        "lowest_price": round(df["low"].min(), 2),
        "avg_volume": int(df["volume"].mean()),
        "total_return_pct": round(
            ((df["close"].iloc[-1] - df["close"].iloc[0]) / df["close"].iloc[0]) * 100, 2
        ),
        "avg_daily_return": round(df["daily_return"].mean(), 4) if "daily_return" in df.columns else None,
        "volatility_avg": round(df["volatility"].mean(), 4) if "volatility" in df.columns else None,
    }


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    df = add_moving_averages(df)
    df = add_daily_return(df)
    df = add_volatility(df)
    return df


def print_summary(stats: dict):
    print(f"\n{'='*45}")
    print(f"  Stock: {stats['ticker']}")
    print(f"  Period: {stats['start_date']} to {stats['end_date']} ({stats['total_days']} days)")
    print(f"  Start Price : ${stats['start_price']}")
    print(f"  End Price   : ${stats['end_price']}")
    print(f"  Highest     : ${stats['highest_price']}")
    print(f"  Lowest      : ${stats['lowest_price']}")
    print(f"  Total Return: {stats['total_return_pct']}%")
    print(f"  Avg Volume  : {stats['avg_volume']:,}")
    print(f"{'='*45}")
