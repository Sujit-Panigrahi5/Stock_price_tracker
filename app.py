import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import STOCKS, SHORT_MA, LONG_MA
from src.fetch_data import fetch_stock
from src.store_data import create_table, save_stock_data, load_stock_data, get_available_tickers
from src.analyze import enrich, summary_stats

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Price Tracker",
    page_icon="📈",
    layout="wide",
)

# ── Init DB ───────────────────────────────────────────────────────────────────
create_table()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("📈 Stock Tracker")
st.sidebar.markdown("---")

all_tickers = STOCKS
selected_tickers = st.sidebar.multiselect(
    "Select Stocks",
    options=all_tickers,
    default=["AAPL", "TSLA"],
)

period = st.sidebar.selectbox(
    "Time Period",
    options=["1mo", "3mo", "6mo", "1y", "2y"],
    index=2,
)

if st.sidebar.button("🔄 Fetch Latest Data", use_container_width=True):
    with st.spinner("Fetching data from Yahoo Finance..."):
        for ticker in selected_tickers:
            df = fetch_stock(ticker, period)
            if not df.empty:
                save_stock_data(df)
    st.sidebar.success("Data updated!")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Data sourced from Yahoo Finance via yfinance")

# ── Main ──────────────────────────────────────────────────────────────────────
st.title("Stock Price Tracker")
st.markdown("Track, analyze, and compare stock prices with moving averages and return metrics.")

if not selected_tickers:
    st.warning("Please select at least one stock from the sidebar.")
    st.stop()

# Load and enrich data
stock_data = {}
for ticker in selected_tickers:
    df = load_stock_data(ticker)
    if df.empty:
        st.warning(f"No data for {ticker}. Click 'Fetch Latest Data' in the sidebar.")
        continue
    df = enrich(df)
    stock_data[ticker] = df

if not stock_data:
    st.info("Click '🔄 Fetch Latest Data' in the sidebar to load data.")
    st.stop()

# ── Summary Cards ─────────────────────────────────────────────────────────────
st.subheader("Summary")
cols = st.columns(len(stock_data))

for col, (ticker, df) in zip(cols, stock_data.items()):
    stats = summary_stats(df)
    ret = stats["total_return_pct"]
    color = "green" if ret >= 0 else "red"
    arrow = "▲" if ret >= 0 else "▼"

    col.metric(
        label=f"{ticker}",
        value=f"${stats['end_price']}",
        delta=f"{arrow} {ret}% total return",
    )

st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Price & Moving Averages",
    "📊 Volume",
    "📉 Daily Returns",
    "🔀 Stock Comparison",
])

# ── Tab 1: Price + MA ─────────────────────────────────────────────────────────
with tab1:
    for ticker, df in stock_data.items():
        st.subheader(f"{ticker} — Close Price & Moving Averages")
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=pd.to_datetime(df["date"]),
            y=df["close"],
            name="Close Price",
            line=dict(color="#1f77b4", width=2),
        ))
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(df["date"]),
            y=df[f"MA{SHORT_MA}"],
            name=f"{SHORT_MA}-day MA",
            line=dict(color="#ff7f0e", width=1.5, dash="dash"),
        ))
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(df["date"]),
            y=df[f"MA{LONG_MA}"],
            name=f"{LONG_MA}-day MA",
            line=dict(color="#2ca02c", width=1.5, dash="dash"),
        ))

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode="x unified",
            height=420,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 2: Volume ─────────────────────────────────────────────────────────────
with tab2:
    for ticker, df in stock_data.items():
        st.subheader(f"{ticker} — Trading Volume")
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=pd.to_datetime(df["date"]),
            y=df["volume"],
            name="Volume",
            marker_color="#1f77b4",
            opacity=0.7,
        ))

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Volume",
            hovermode="x unified",
            height=380,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 3: Daily Return ───────────────────────────────────────────────────────
with tab3:
    for ticker, df in stock_data.items():
        st.subheader(f"{ticker} — Daily Return (%)")
        returns = df["daily_return"].fillna(0)
        colors = ["#2ca02c" if r >= 0 else "#d62728" for r in returns]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=pd.to_datetime(df["date"]),
            y=returns,
            name="Daily Return",
            marker_color=colors,
            opacity=0.85,
        ))
        fig.add_hline(y=0, line_color="black", line_width=0.8)

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Return (%)",
            hovermode="x unified",
            height=380,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 4: Comparison ─────────────────────────────────────────────────────────
with tab4:
    st.subheader("Stock Comparison — Normalized Price (Base = 100)")
    fig = go.Figure()

    for ticker, df in stock_data.items():
        normalized = (df["close"] / df["close"].iloc[0]) * 100
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(df["date"]),
            y=normalized,
            name=ticker,
            line=dict(width=2),
        ))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Normalized Price (Base = 100)",
        hovermode="x unified",
        height=450,
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Return table
    st.subheader("Return Summary")
    rows = []
    for ticker, df in stock_data.items():
        stats = summary_stats(df)
        rows.append({
            "Ticker": stats["ticker"],
            "Start Date": stats["start_date"],
            "End Date": stats["end_date"],
            "Start Price ($)": stats["start_price"],
            "End Price ($)": stats["end_price"],
            "Highest ($)": stats["highest_price"],
            "Lowest ($)": stats["lowest_price"],
            "Total Return (%)": stats["total_return_pct"],
            "Avg Volume": f"{stats['avg_volume']:,}",
        })

    summary_df = pd.DataFrame(rows)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
