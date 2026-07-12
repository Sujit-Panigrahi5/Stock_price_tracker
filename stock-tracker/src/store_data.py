import sqlite3
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH


def get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker    TEXT NOT NULL,
            date      TEXT NOT NULL,
            open      REAL,
            high      REAL,
            low       REAL,
            close     REAL,
            volume    INTEGER,
            UNIQUE(ticker, date)
        )
    """)
    conn.commit()
    conn.close()


def save_stock_data(df: pd.DataFrame):
    if df.empty:
        print("  Nothing to save.")
        return

    conn = get_connection()
    saved = 0
    skipped = 0

    for _, row in df.iterrows():
        try:
            conn.execute("""
                INSERT OR IGNORE INTO stock_prices (ticker, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row["Ticker"],
                str(row["Date"]),
                row["Open"],
                row["High"],
                row["Low"],
                row["Close"],
                int(row["Volume"])
            ))
            if conn.execute("SELECT changes()").fetchone()[0]:
                saved += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  Error saving row: {e}")

    conn.commit()
    conn.close()
    print(f"  Saved {saved} new rows, skipped {skipped} duplicates.")


def load_stock_data(ticker: str = None) -> pd.DataFrame:
    conn = get_connection()
    if ticker:
        df = pd.read_sql_query(
            "SELECT * FROM stock_prices WHERE ticker = ? ORDER BY date ASC",
            conn,
            params=(ticker,)
        )
    else:
        df = pd.read_sql_query(
            "SELECT * FROM stock_prices ORDER BY ticker, date ASC",
            conn
        )
    conn.close()
    return df


def get_available_tickers() -> list:
    conn = get_connection()
    cursor = conn.execute("SELECT DISTINCT ticker FROM stock_prices ORDER BY ticker")
    tickers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tickers
