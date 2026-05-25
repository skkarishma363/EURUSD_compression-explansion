import pandas as pd


def run_synchronized_backtest(

    sync_trades,

    df_m5,

    atr_multiplier=2.0,

    tp1_multiplier=1.5

):
    completed_trades = []

    # =========================
    # ACCOUNT / EXECUTION SETTINGS
    # =========================
    account_balance = 10000.0
    risk_per_trade = 0.01
    spread = 0.00010
    slippage = 0.00003

    # Loop through synchronized entries
    for i in range(len(sync_trades)):
        trade = sync_trades.iloc[i]
        trade_type = trade["Type"]
        entry_time = trade["EntryTime"]

        # Find entry row in M5 dataframe
        if entry_time not in df_m5.index:
            continue

        entry_index = df_m5.index.get_loc(entry_time)

        # BUY
        if trade_type == "BUY":
            entry_price = trade["EntryPrice"] + spread + slippage
            atr = df_m5.iloc[entry_index]["ATR"]
            stop_distance = atr * 1.2
            risk_amount = account_balance * risk_per_trade
            position_size = risk_amount / stop_distance if stop_distance != 0 else 0

            stop_loss = entry_price - stop_distance
            tp1 = entry_price + (tp1_multiplier * stop_distance)
            tp2 = entry_price + 2 * stop_distance

            tp1_hit = False
            trailing_active = False
            trailing_stop = stop_loss

            for j in range(entry_index + 1, min(entry_index + 50, len(df_m5))):
                future_high = df_m5.iloc[j]["High"]
                future_low = df_m5.iloc[j]["Low"]
                exit_time = df_m5.index[j]

                if not tp1_hit and future_high >= tp1:
                    tp1_hit = True
                    stop_loss = entry_price

                if tp1_hit and not trailing_active and future_high >= tp2:
                    trailing_active = True

                if trailing_active:
                    current_atr = df_m5.iloc[j]["ATR"]
                    new_trailing_stop = future_high - (atr_multiplier * current_atr)
                    trailing_stop = max(trailing_stop, new_trailing_stop)

                    if future_low <= trailing_stop:
                        profit = (
                            0.5 * (tp1 - entry_price)
                            + 0.5 * ((trailing_stop - spread) - entry_price)
                        ) * position_size

                        account_balance += profit
                        completed_trades.append({
                            "Type": "BUY",
                            "EntryTime": entry_time,
                            "ExitTime": exit_time,
                            "Entry": entry_price,
                            "SL": trailing_stop,
                            "TP": "ATR_TRAIL",
                            "Result": "WIN",
                            "Profit": profit,
                            "Balance": account_balance,
                        })
                        break

                elif future_low <= stop_loss:
                    if not tp1_hit:
                        profit = (stop_loss - entry_price) * position_size
                        result = "LOSS"
                    else:
                        profit = 0.5 * ((tp1 - spread) - entry_price) * position_size
                        result = "BREAKEVEN"

                    account_balance += profit
                    completed_trades.append({
                        "Type": "BUY",
                        "EntryTime": entry_time,
                        "ExitTime": exit_time,
                        "Entry": entry_price,
                        "SL": stop_loss,
                        "TP": tp2,
                        "Result": result,
                        "Profit": profit,
                        "Balance": account_balance,
                    })
                    break

        # SELL
        elif trade_type == "SELL":
            entry_price = trade["EntryPrice"] - spread - slippage
            atr = df_m5.iloc[entry_index]["ATR"]
            stop_distance = atr * 1.2
            risk_amount = account_balance * risk_per_trade
            position_size = risk_amount / stop_distance if stop_distance != 0 else 0

            stop_loss = entry_price + stop_distance
            tp1 = entry_price - (tp1_multiplier * stop_distance)
            tp2 = entry_price - 2 * stop_distance

            tp1_hit = False
            trailing_active = False
            trailing_stop = stop_loss

            # Scan future candles
            for j in range(entry_index + 1, min(entry_index + 50, len(df_m5))):
                future_high = df_m5.iloc[j]["High"]
                future_low = df_m5.iloc[j]["Low"]
                exit_time = df_m5.index[j]

                if not tp1_hit and future_low <= tp1:
                    tp1_hit = True
                    stop_loss = entry_price

                if tp1_hit and not trailing_active and future_low <= tp2:
                    trailing_active = True

                if trailing_active:
                    current_atr = df_m5.iloc[j]["ATR"]
                    new_trailing_stop = future_low + (atr_multiplier * current_atr)
                    trailing_stop = min(trailing_stop, new_trailing_stop)

                    if future_high >= trailing_stop:
                        profit = (
                            0.5 * (entry_price - tp1)
                            + 0.5 * (entry_price - (trailing_stop + spread))
                        ) * position_size

                        account_balance += profit
                        completed_trades.append({
                            "Type": "SELL",
                            "EntryTime": entry_time,
                            "ExitTime": exit_time,
                            "Entry": entry_price,
                            "SL": trailing_stop,
                            "TP": "ATR_TRAIL",
                            "Result": "WIN",
                            "Profit": profit,
                            "Balance": account_balance,
                        })
                        break
                elif future_high >= stop_loss:
                    if not tp1_hit:
                        profit = (entry_price - stop_loss) * position_size
                        result = "LOSS"
                    else:
                        profit = 0.5 * (entry_price - (tp1 + spread)) * position_size
                        result = "BREAKEVEN"

                    account_balance += profit
                    completed_trades.append({
                        "Type": "SELL",
                        "EntryTime": entry_time,
                        "ExitTime": exit_time,
                        "Entry": entry_price,
                        "SL": stop_loss,
                        "TP": tp2,
                        "Result": result,
                        "Profit": profit,
                        "Balance": account_balance,
                    })
                    break

    results_df = pd.DataFrame(completed_trades)
    return results_df