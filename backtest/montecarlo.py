import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def run_monte_carlo(

    trades_df,

    simulations=1000

):

    print("\n===== MONTE CARLO SIMULATION =====")

    # ====================================
    # EXTRACT PROFITS
    # ====================================

    profits = trades_df["Profit"].values

    if len(profits) == 0:

        print("No trades available.")

        return

    equity_curves = []

    final_balances = []

    max_drawdowns = []

    # ====================================
    # RUN SIMULATIONS
    # ====================================

    for i in range(simulations):

        # Random reshuffle
        shuffled = np.random.choice(

            profits,

            size=len(profits),

            replace=True

        )

        equity = 10000 + np.cumsum(shuffled)

        equity_curves.append(equity)

        final_balances.append(equity[-1])

        # Drawdown
        peak = np.maximum.accumulate(equity)

        drawdown = equity - peak

        max_drawdowns.append(drawdown.min())

    # ====================================
    # SUMMARY
    # ====================================

    print(f"Simulations: {simulations}")

    print(
        f"Average Final Balance: "
        f"{np.mean(final_balances):.2f}"
    )

    print(
        f"Worst Final Balance: "
        f"{np.min(final_balances):.2f}"
    )

    print(
        f"Best Final Balance: "
        f"{np.max(final_balances):.2f}"
    )

    print(
        f"Average Max Drawdown: "
        f"{np.mean(max_drawdowns):.2f}"
    )

    # ====================================
    # PLOT EQUITY CURVES
    # ====================================

    return {

    "equity_curves": equity_curves,

    "final_balances": final_balances,

    "max_drawdowns": max_drawdowns,

    "avg_balance": np.mean(final_balances),

    "worst_balance": np.min(final_balances),

    "best_balance": np.max(final_balances),

    "avg_drawdown": np.mean(max_drawdowns)

}