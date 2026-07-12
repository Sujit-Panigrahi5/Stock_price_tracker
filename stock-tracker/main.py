import sys
import os

from config import STOCKS
from src.fetch_data import fetch_all_stocks
from src.store_data import create_table, save_stock_data, load_stock_data, get_available_tickers
from src.analyze import enrich, summary_stats, print_summary
from src.visualize import plot_all_for_ticker, plot_comparison


def run():
    print("\n====== Stock Price Tracker ======\n")

    # Step 1 — Setup DB
    print("[1/4] Setting up database...")
    create_table()
    print("  Database ready.")

    # Step 2 — Fetch data
    print("\n[2/4] Fetching stock data...")
    raw_df = fetch_all_stocks(STOCKS)

    # Step 3 — Save to SQLite
    print("\n[3/4] Saving to database...")
    save_stock_data(raw_df)

    # Step 4 — Analyze and visualize
    print("\n[4/4] Analyzing and generating charts...")
    tickers = get_available_tickers()

    if not tickers:
        print("  No data in database. Exiting.")
        return

    all_enriched = {}

    for ticker in tickers:
        df = load_stock_data(ticker)

        if df.empty:
            continue

        df = enrich(df)
        stats = summary_stats(df)
        print_summary(stats)

        plot_all_for_ticker(df, ticker)
        all_enriched[ticker] = df

    # Comparison chart across all stocks
    if len(all_enriched) > 1:
        print("\n  Generating comparison chart...")
        plot_comparison(all_enriched)

    print("\n====== Done! Charts saved in /charts folder ======\n")


if __name__ == "__main__":
    run()
