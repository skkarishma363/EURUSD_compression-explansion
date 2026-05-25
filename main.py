from utils.loader import load_forex_data
from utils.resampler import resample_timeframes
from utils.cleaner import clean_data
from strategy.indicators import apply_indicators
from strategy.compression import apply_compression
from strategy.breakout import apply_breakouts
from strategy.pullback import apply_pullbacks
from strategy.pullback import scan_pullbacks
from strategy.entries import apply_entries
from strategy.risk import apply_risk_management
from backtest.engine import run_synchronized_backtest
from backtest.synchronizer import synchronize_entries
from backtest.visualization import (
    plot_equity_curve,
    plot_win_loss,
    plot_profit_distribution
)
from strategy.sessions import add_session_filter
from backtest.metrics import calculate_metrics
from backtest.walkforward import (
    run_walk_forward_tests
)
from backtest.optimizer import run_grid_search
from backtest.montecarlo import (
    run_monte_carlo
)
# Load raw data
df = load_forex_data("data/raw")

# Clean data
df = clean_data(df)

# Create timeframes
df_m5, df_h1 = resample_timeframes(df)
# Apply indicators
df_m5 = apply_indicators(df_m5)
# Apply entry logic on M5
df_m5 = apply_entries(df_m5)
df_h1 = apply_indicators(df_h1)
# Apply compression detection
df_h1 = apply_compression(df_h1)
# Apply breakout detection
df_h1 = apply_breakouts(df_h1)
# Apply pullback logic
df_h1 = apply_pullbacks(df_h1)
# Apply risk management
df_h1 = apply_risk_management(df_h1)
# Apply session filter
df_h1 = add_session_filter(df_h1)
# Scan for pullback opportunities
buy_pullbacks, sell_pullbacks = scan_pullbacks(df_h1)
# Synchronize H1 and M5
sync_trades = synchronize_entries(
    df_h1,
    df_m5,
    buy_pullbacks,
    sell_pullbacks
)
# Keep only valid session trades
valid_trade_times = df_h1[
    df_h1["ValidSession"]
].index

sync_trades = sync_trades[
    sync_trades["EntryTime"]
    .dt.floor("h")
    .isin(valid_trade_times)
]
# Show outputs
# Run backtest
trades_df = run_synchronized_backtest(
    sync_trades,
    df_m5
)
print("\n===== PULLBACKS =====")
print("\n===== BUY PULLBACKS =====")

print(buy_pullbacks[-10:])

print("\n===== SELL PULLBACKS =====")

print(sell_pullbacks[-10:])
entry_signals = df_m5[

    (
        df_m5["BullishEngulfing"]
    )

    |

    (
        df_m5["BearishEngulfing"]
    )

]

print("\n===== ENTRY SIGNALS =====")

print(
    entry_signals[
        [
            "Close",
            "BullishEngulfing",
            "BearishEngulfing",
            "BreakSwingHigh",
            "BreakSwingLow"
        ]
    ].tail(20)
)
print("\n===== RISK MANAGEMENT =====")

print(
    df_h1[
        [
            "Close",
            "BuySL",
            "SellSL",
            "BuyTP1",
            "BuyTP2",
            "SellTP1",
            "SellTP2"
        ]
    ].tail(10)
)
print("\n===== BACKTEST RESULTS =====")

print(trades_df.tail(20))
# Total trades
total_trades = len(trades_df)

# Wins
wins = len(
    trades_df[
        trades_df["Result"] == "WIN"
    ]
)

# Losses
losses = len(
    trades_df[
        trades_df["Result"] == "LOSS"
    ]
)
breakevens = len(
    trades_df[
        trades_df["Result"] == "BREAKEVEN"
    ]
)
# Win rate
win_rate = (
    (wins / total_trades) * 100
    if total_trades > 0
    else 0
)

# Total profit
total_profit = (
    trades_df["Profit"].sum()
)

print("\n===== STATISTICS =====")

print(f"Total Trades: {total_trades}")

print(f"Wins: {wins}")

print(f"Losses: {losses}")

print(f"Breakevens: {breakevens}")

print(f"Win Rate: {win_rate:.2f}%")

print(f"Total Profit: {total_profit:.5f}")
# Total trades
total_trades = len(trades_df)

# Wins
wins = len(
    trades_df[
        trades_df["Result"] == "WIN"
    ]
)

# Losses
losses = len(
    trades_df[
        trades_df["Result"] == "LOSS"
    ]
)

# Win rate
win_rate = (
    (wins / total_trades) * 100
    if total_trades > 0
    else 0
)

# Total profit
total_profit = (
    trades_df["Profit"].sum()
)

print("\n===== SYNCHRONIZED TRADES =====")

print(sync_trades.tail(20))
# Plot charts
plot_equity_curve(trades_df)

plot_win_loss(trades_df)

plot_profit_distribution(trades_df)
print("\n===== SESSION FILTER =====")

print(
    f"Trades After Session Filter: "
    f"{len(sync_trades)}"
)
calculate_metrics(trades_df)
run_walk_forward_tests(

    sync_trades,

    df_m5

)
run_grid_search(

    df_h1,

    df_m5,

    buy_pullbacks,

    sell_pullbacks

)
run_monte_carlo(

    trades_df,

    simulations=1000

)