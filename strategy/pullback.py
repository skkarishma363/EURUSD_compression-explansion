def calculate_breakout_move(df):

    # BUY breakout move
    df["BuyBreakoutMove"] = (
        df["Close"] -
        df["RangeHigh"]
    )

    # SELL breakout move
    df["SellBreakoutMove"] = (
        df["RangeLow"] -
        df["Close"]
    )

    return df
def add_buy_pullback_zone(df):

    # 30% retracement
    df["BuyPullback30"] = (
        df["Close"] -
        (df["BuyBreakoutMove"] * 0.30)
    )

    # 60% retracement
    df["BuyPullback60"] = (
        df["Close"] -
        (df["BuyBreakoutMove"] * 0.60)
    )

    return df
def add_sell_pullback_zone(df):

    # 30% retracement
    df["SellPullback30"] = (
        df["Close"] +
        (df["SellBreakoutMove"] * 0.30)
    )

    # 60% retracement
    df["SellPullback60"] = (
        df["SellBreakoutMove"] * 0.60
        +
        df["Close"]
    )

    return df
def detect_buy_pullback(df):

    df["BuyPullbackTouched"] = (

        (df["Low"] <= df["BuyPullback30"])

        &

        (df["Low"] >= df["BuyPullback60"])

    )

    return df
def detect_sell_pullback(df):

    df["SellPullbackTouched"] = (

        (df["High"] >= df["SellPullback30"])

        &

        (df["High"] <= df["SellPullback60"])

    )

    return df
def apply_pullbacks(df):

    df = calculate_breakout_move(df)

    df = add_buy_pullback_zone(df)

    df = add_sell_pullback_zone(df)

    df = detect_buy_pullback(df)

    df = detect_sell_pullback(df)

    # df = add_final_pullbacks(df)

    return df
def scan_pullbacks(df):

    buy_pullbacks = []

    sell_pullbacks = []

    # Loop through candles
    for i in range(len(df)):

        # -------------------------
        # BUY BREAKOUT
        # -------------------------

        if df.iloc[i]["FinalBuyBreakout"]:

            breakout_close = df.iloc[i]["Close"]

            breakout_move = df.iloc[i]["BuyBreakoutMove"]

            pullback30 = (
                breakout_close -
                (breakout_move * 0.30)
            )

            pullback60 = (
                breakout_close -
                (breakout_move * 0.60)
            )

            # Scan future candles
            for j in range(i + 1, min(i + 10, len(df))):

                current_low = df.iloc[j]["Low"]

                if (
                    current_low <= pullback30
                    and
                    current_low >= pullback60
                ):

                    buy_pullbacks.append(
                        df.index[j]
                    )

                    break

        # -------------------------
        # SELL BREAKOUT
        # -------------------------

        if df.iloc[i]["FinalSellBreakout"]:

            breakout_close = df.iloc[i]["Close"]

            breakout_move = df.iloc[i]["SellBreakoutMove"]

            pullback30 = (
                breakout_close +
                (breakout_move * 0.30)
            )

            pullback60 = (
                breakout_close +
                (breakout_move * 0.60)
            )

            # Scan future candles
            for j in range(i + 1, min(i + 10, len(df))):

                current_high = df.iloc[j]["High"]

                if (
                    current_high >= pullback30
                    and
                    current_high <= pullback60
                ):

                    sell_pullbacks.append(
                        df.index[j]
                    )

                    break

    return buy_pullbacks, sell_pullbacks