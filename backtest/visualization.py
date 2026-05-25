import matplotlib.pyplot as plt
def plot_equity_curve(trades_df):

    # Cumulative profit
    trades_df["EquityCurve"] = (
        trades_df["Profit"].cumsum()
    )

    # Create chart
    plt.figure(figsize=(12, 6))

    plt.plot(
        trades_df["EquityCurve"]
    )

    plt.title(
        "Equity Curve"
    )

    plt.xlabel(
        "Trades"
    )

    plt.ylabel(
        "Profit"
    )

    plt.grid(True)

    plt.show()
def plot_win_loss(trades_df):

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

    plt.figure(figsize=(6, 6))

    plt.pie(
        [wins, losses],
        labels=["Wins", "Losses"],
        autopct="%1.1f%%"
    )

    plt.title(
        "Win vs Loss Distribution"
    )

    plt.show()
def plot_profit_distribution(trades_df):

    plt.figure(figsize=(10, 5))

    plt.hist(
        trades_df["Profit"],
        bins=20
    )

    plt.title(
        "Profit Distribution"
    )

    plt.xlabel(
        "Profit"
    )

    plt.ylabel(
        "Frequency"
    )

    plt.grid(True)

    plt.show()
