import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.loader import load_forex_data
from utils.cleaner import clean_data
from utils.resampler import resample_timeframes

from strategy.indicators import apply_indicators
from strategy.compression import apply_compression
from strategy.breakout import apply_breakouts
from strategy.pullback import (
    apply_pullbacks,
    scan_pullbacks
)
from strategy.entries import apply_entries
from strategy.risk import apply_risk_management
from strategy.sessions import add_session_filter

from backtest.synchronizer import synchronize_entries
from backtest.engine import run_synchronized_backtest
from backtest.metrics import calculate_metrics
from backtest.montecarlo import run_monte_carlo

from backtest.optimizer import run_grid_search
# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(
    page_title="EURUSD Quant Dashboard",
    layout="wide"
)

# ====================================
# TITLE
# ====================================

st.title("📈 EURUSD Quant Research Dashboard")

st.markdown(
    "Volatility Compression → Expansion Strategy"
)

# ====================================
# SIDEBAR
# ====================================

st.sidebar.header("Strategy Parameters")

adx_threshold = st.sidebar.slider(
    "ADX Threshold",
    10,
    40,
    30
)

ema_distance = st.sidebar.slider(
    "EMA Distance",
    0.05,
    0.50,
    0.15
)

tp1_multiplier = st.sidebar.slider(
    "TP1 Multiplier",
    1.0,
    3.0,
    2.0
)

atr_multiplier = st.sidebar.slider(
    "ATR Trail Multiplier",
    1.0,
    3.0,
    1.5
)

# ====================================
# LOAD DATA
# ====================================

with st.spinner("Loading market data..."):

    df = load_forex_data("data/raw")

    df = clean_data(df)

    df_m5, df_h1 = resample_timeframes(df)

# ====================================
# APPLY STRATEGY
# ====================================

df_m5 = apply_indicators(df_m5)

df_m5 = apply_entries(df_m5)

df_h1 = apply_indicators(df_h1)

df_h1 = apply_compression(df_h1)

df_h1 = apply_breakouts(
    df_h1,
    adx_threshold=adx_threshold,
    ema_distance_threshold=ema_distance
)

df_h1 = apply_pullbacks(df_h1)

df_h1 = apply_risk_management(df_h1)

df_h1 = add_session_filter(df_h1)

buy_pullbacks, sell_pullbacks = scan_pullbacks(df_h1)

sync_trades = synchronize_entries(
    df_h1,
    df_m5,
    buy_pullbacks,
    sell_pullbacks
)

# ====================================
# RUN BACKTEST
# ====================================

trades_df = run_synchronized_backtest(
    sync_trades,
    df_m5,
    atr_multiplier=atr_multiplier,
    tp1_multiplier=tp1_multiplier
)

# ====================================
# METRICS
# ====================================

total_trades = len(trades_df)

wins = len(
    trades_df[
        trades_df["Result"] == "WIN"
    ]
)

losses = len(
    trades_df[
        trades_df["Result"] == "LOSS"
    ]
)

win_rate = (
    (wins / total_trades) * 100
    if total_trades > 0
    else 0
)

net_profit = trades_df["Profit"].sum()
# ====================================
# DASHBOARD TABS
# ====================================

overview_tab, trades_tab, optimization_tab, montecarlo_tab = st.tabs([

    "Overview",

    "Trades",

    "Optimization",

    "Monte Carlo"

])
with overview_tab:

# ====================================
# TOP METRICS
# ====================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Trades",
        total_trades
    )

    col2.metric(
        "Win Rate",
        f"{win_rate:.2f}%"
    )

    col3.metric(
        "Net Profit",
        f"{net_profit:.2f}"
    )

    profit_factor = (
        trades_df[
            trades_df["Profit"] > 0
        ]["Profit"].sum()
        /
        abs(
            trades_df[
                trades_df["Profit"] < 0
            ]["Profit"].sum()
        )
        if len(
            trades_df[
                trades_df["Profit"] < 0
            ]
        ) > 0
        else 0
    )

    col4.metric(
        "Profit Factor",
        f"{profit_factor:.2f}"
    )

# ====================================
# EQUITY CURVE
# ====================================

    st.subheader("Equity Curve")

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            y=trades_df["Balance"],

            mode="lines",

            name="Balance"

        )

    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
with trades_tab:
# ====================================
# TRADE TABLE
# ====================================

    st.subheader("Trade Log")
    # ====================================
    # CANDLESTICK TRADE VIEW
    # ====================================

    st.subheader("Trade Candlestick View")
    chart_data = df_m5.tail(300)
    chart_start = chart_data.index.min()

    chart_end = chart_data.index.max()
    # Last 300 candles
    

    candlestick_fig = go.Figure()

    # ====================================
    # CANDLESTICKS
    # ====================================

    candlestick_fig.add_trace(

        go.Candlestick(

            x=chart_data.index,

            open=chart_data["Open"],

            high=chart_data["High"],

            low=chart_data["Low"],

            close=chart_data["Close"],

            name="Price"

        )

    )

    # ====================================
    # BUY TRADES
    # ====================================

    buy_trades = sync_trades[
        sync_trades["Type"] == "BUY"
    ]

    candlestick_fig.add_trace(

        go.Scatter(

            x=buy_trades["EntryTime"],

            y=buy_trades["EntryPrice"],

            mode="markers",

            marker=dict(

                size=12,

                symbol="triangle-up",

                color="green"

            ),

            name="BUY"

        )

    )

    # ====================================
    # SELL TRADES
    # ====================================

    sell_trades = sync_trades[
        sync_trades["Type"] == "SELL"
    ]

    candlestick_fig.add_trace(

        go.Scatter(

            x=sell_trades["EntryTime"],

            y=sell_trades["EntryPrice"],

            mode="markers",

            marker=dict(

                size=12,

                symbol="triangle-down",

                color="red"

            ),

            name="SELL"

        )

    )

    # ====================================
    # LAYOUT
    # ====================================

    candlestick_fig.update_layout(

        height=700,

        xaxis_rangeslider_visible=False

    )

    st.plotly_chart(

        candlestick_fig,

        use_container_width=True

    )
    st.dataframe(
        trades_df.tail(20),
        use_container_width=True
    )

# ====================================
# PROFIT DISTRIBUTION
# ====================================

    st.subheader("Profit Distribution")

    hist_fig = px.histogram(
        trades_df,
        x="Profit",
        nbins=20
    )

    st.plotly_chart(
        hist_fig,
        use_container_width=True
    )
with optimization_tab:

    st.subheader("Optimization Results")

    with st.spinner(
        "Running grid search optimization..."
    ):

        optimization_results = run_grid_search(

            df_h1,

            df_m5,

            buy_pullbacks,

            sell_pullbacks

        )

    # ====================================
    # BEST PARAMETERS
    # ====================================

    best_row = optimization_results.iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Best ATR",
        best_row["ATR"]
    )

    c2.metric(
        "Best TP1",
        best_row["TP1"]
    )

    c3.metric(
        "Best ADX",
        best_row["ADX"]
    )

    c4.metric(
        "Best Profit Factor",
        f"{best_row['ProfitFactor']:.2f}"
    )

    # ====================================
    # RESULTS TABLE
    # ====================================

    st.subheader("Top Optimization Results")

    st.dataframe(

        optimization_results.head(20),

        use_container_width=True

    )
with montecarlo_tab:

    st.subheader("Monte Carlo Analysis")

    monte_results = run_monte_carlo(

        trades_df,

        simulations=500

    )

    # ====================================
    # METRICS
    # ====================================

    mc1, mc2, mc3, mc4 = st.columns(4)

    mc1.metric(

        "Average Balance",

        f"{monte_results['avg_balance']:.2f}"

    )

    mc2.metric(

        "Worst Balance",

        f"{monte_results['worst_balance']:.2f}"

    )

    mc3.metric(

        "Best Balance",

        f"{monte_results['best_balance']:.2f}"

    )

    mc4.metric(

        "Average Drawdown",

        f"{monte_results['avg_drawdown']:.2f}"

    )

    # ====================================
    # PLOTLY CHART
    # ====================================

    mc_fig = go.Figure()

    for curve in monte_results["equity_curves"][:100]:

        mc_fig.add_trace(

            go.Scatter(

                y=curve,

                mode="lines",

                opacity=0.15,

                showlegend=False

            )

        )

    mc_fig.update_layout(

        title="Monte Carlo Equity Simulations",

        height=600

    )

    st.plotly_chart(

        mc_fig,

        use_container_width=True

    )