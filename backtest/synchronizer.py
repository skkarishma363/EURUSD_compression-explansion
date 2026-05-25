import pandas as pd
def synchronize_entries(
    df_h1,
    df_m5,
    buy_pullbacks,
    sell_pullbacks
):

    synchronized_trades = []

    # =========================
    # BUY PULLBACKS
    # =========================

    for timestamp in buy_pullbacks:

        # Pullback window
        start_time = timestamp

        end_time = (
            timestamp +
            pd.Timedelta(hours=4)
        )

        # M5 data inside window
        m5_window = df_m5.loc[
            start_time:end_time
        ]

        # Search M5 confirmations
        for i in range(len(m5_window)):

            row = m5_window.iloc[i]

            bullish_signal = (

                row["BullishEngulfing"]

                or

                row["BreakSwingHigh"]

            )

            if bullish_signal:

                synchronized_trades.append({

                    "Type": "BUY",

                    "EntryTime": m5_window.index[i],

                    "EntryPrice": row["Close"]

                })

                break

    # =========================
    # SELL PULLBACKS
    # =========================

    for timestamp in sell_pullbacks:

        start_time = timestamp

        end_time = (
            timestamp +
            pd.Timedelta(hours=4)
        )

        m5_window = df_m5.loc[
            start_time:end_time
        ]

        # Search confirmations
        for i in range(len(m5_window)):

            row = m5_window.iloc[i]

            bearish_signal = (

                row["BearishEngulfing"]

                or

                row["BreakSwingLow"]

            )

            if bearish_signal:

                synchronized_trades.append({

                    "Type": "SELL",

                    "EntryTime": m5_window.index[i],

                    "EntryPrice": row["Close"]

                })

                break

    # Convert to dataframe
    trades_df = pd.DataFrame(
        synchronized_trades
    )

    return trades_df