import itertools
import pandas as pd
from strategy.breakout import apply_breakouts

from strategy.pullback import apply_pullbacks

from strategy.pullback import scan_pullbacks

from strategy.entries import apply_entries

from backtest.engine import run_synchronized_backtest
from backtest.synchronizer import synchronize_entries

# from backtest.metrics import (
#     calculate_metrics
# )
def run_grid_search(

    df_h1,

    df_m5,

    buy_pullbacks,

    sell_pullbacks

):

    print("\n===== GRID SEARCH OPTIMIZATION =====")

    # ====================================
    # PARAMETER RANGES
    # ====================================

    atr_values = [1.5, 2.0]

    tp1_values = [1.5, 2.0]

    adx_values = [20, 30]

    ema_distance_values = [0.10, 0.20]

    # ====================================
    # ALL COMBINATIONS
    # ====================================

    combinations = list(

        itertools.product(

            atr_values,

            tp1_values,

            adx_values,

            ema_distance_values

        )

    )

    results = []

    # ====================================
    # LOOP COMBINATIONS
    # ====================================

    for combo in combinations:

        atr_mult, tp1_mult, adx_filter, ema_dist = combo

        print("\n--------------------------")
        print(f"ATR: {atr_mult}")
        print(f"TP1: {tp1_mult}")
        print(f"ADX: {adx_filter}")
        print(f"EMA DIST: {ema_dist}")

        # ====================================
        # RUN BACKTEST
        # ====================================

        # ====================================
            # REBUILD STRATEGY
# ====================================

        df_temp = apply_breakouts(

            df_h1.copy(),

            adx_threshold=adx_filter,

            ema_distance_threshold=ema_dist

        )

        df_temp = apply_pullbacks(df_temp)

        df_m5_temp = apply_entries(

            df_m5.copy()

        )
        # ====================================
# DYNAMIC PULLBACK SCANNING
# ====================================

        buy_pullbacks_temp, sell_pullbacks_temp = scan_pullbacks(

            df_temp

)
        sync_trades_temp = synchronize_entries(

            df_temp,

            df_m5_temp,

            buy_pullbacks_temp,

            sell_pullbacks_temp

)
        trades_df = run_synchronized_backtest(

              sync_trades_temp,

              df_m5_temp,

              atr_multiplier=atr_mult,

              tp1_multiplier=tp1_mult

         )

        # ====================================
        # RUN BACKTEST
        # ====================================


        # ====================================
        # SKIP EMPTY
        # ====================================

        if len(trades_df) == 0:

            continue

        # ====================================
        # METRICS
        # ====================================

        gross_profit = trades_df[
            trades_df["Profit"] > 0
        ]["Profit"].sum()

        gross_loss = abs(

            trades_df[
                trades_df["Profit"] < 0
            ]["Profit"].sum()

        )

        profit_factor = (

            gross_profit / gross_loss

            if gross_loss != 0

            else 0

        )

        net_profit = (
            trades_df["Profit"].sum()
        )

        max_drawdown = (

            trades_df["Balance"].min()

        )

        # ====================================
        # SAVE RESULTS
        # ====================================

        results.append({

            "ATR": atr_mult,

            "TP1": tp1_mult,

            "ADX": adx_filter,

            "EMA_Distance": ema_dist,

            "ProfitFactor": profit_factor,

            "NetProfit": net_profit,

            "MaxDrawdown": max_drawdown

        })

    # ====================================
    # RESULTS DATAFRAME
    # ====================================

    results_df = pd.DataFrame(results)

    # ====================================
    # SORT BEST RESULTS
    # ====================================

    results_df = results_df.sort_values(

        by="ProfitFactor",

        ascending=False

    )

    print("\n===== BEST PARAMETER SETS =====")

    print(results_df.head(10))

    return results_df
