import numpy as np
def calculate_metrics(trades_df):

    # =========================
    # BASIC COUNTS
    # =========================

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

    breakevens = len(
        trades_df[
            trades_df["Result"] == "BREAKEVEN"
        ]
    )

    win_rate = (
        wins / total_trades * 100
        if total_trades > 0
        else 0
    )

    # =========================
    # PROFITS
    # =========================

    gross_profit = trades_df[
        trades_df["Profit"] > 0
    ]["Profit"].sum()

    gross_loss = abs(
        trades_df[
            trades_df["Profit"] < 0
        ]["Profit"].sum()
    )

    net_profit = (
        trades_df["Profit"].sum()
    )

    # =========================
    # PROFIT FACTOR
    # =========================

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss != 0
        else 0
    )

    # =========================
    # EXPECTANCY
    # =========================

    expectancy = (
        net_profit / total_trades
        if total_trades > 0
        else 0
    )

    # =========================
    # AVG WIN / LOSS
    # =========================

    avg_win = trades_df[
        trades_df["Profit"] > 0
    ]["Profit"].mean()

    avg_loss = trades_df[
        trades_df["Profit"] < 0
    ]["Profit"].mean()

    # =========================
    # MAX DRAWDOWN
    # =========================

    equity_curve = (
        trades_df["Balance"]
    )

    running_max = (
        equity_curve.cummax()
    )

    drawdown = (
        equity_curve -
        running_max
    )

    max_drawdown = (
        drawdown.min()
    )

    # =========================
    # SHARPE RATIO
    # =========================

    sharpe_ratio = (
        trades_df["Profit"].mean()
        /
        trades_df["Profit"].std()
        if trades_df["Profit"].std() != 0
        else 0
    )

    # =========================
    # PRINT RESULTS
    # =========================

    print("\n===== ADVANCED METRICS =====")

    print(f"Total Trades: {total_trades}")

    print(f"Wins: {wins}")

    print(f"Losses: {losses}")

    print(f"Breakevens: {breakevens}")

    print(f"Win Rate: {win_rate:.2f}%")

    print(f"Net Profit: {net_profit:.2f}")

    print(f"Gross Profit: {gross_profit:.2f}")

    print(f"Gross Loss: {gross_loss:.2f}")

    print(f"Profit Factor: {profit_factor:.2f}")

    print(f"Expectancy: {expectancy:.2f}")

    print(f"Average Win: {avg_win:.2f}")

    print(f"Average Loss: {avg_loss:.2f}")

    print(f"Max Drawdown: {max_drawdown:.2f}")

    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
