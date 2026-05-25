def add_bullish_engulfing(df):

    # Previous candle
    df["PrevOpen"] = (
        df["Open"].shift(1)
    )

    df["PrevClose"] = (
        df["Close"].shift(1)
    )

    # Bullish engulfing
    df["BullishEngulfing"] = (

        # Previous bearish
        (df["PrevClose"] < df["PrevOpen"])

        &

        # Current bullish
        (df["Close"] > df["Open"])

        &

        # Body engulf
        (df["Open"] < df["PrevClose"])

        &

        (df["Close"] > df["PrevOpen"])

    )

    return df
def add_bearish_engulfing(df):

    df["BearishEngulfing"] = (

        # Previous bullish
        (df["PrevClose"] > df["PrevOpen"])

        &

        # Current bearish
        (df["Close"] < df["Open"])

        &

        # Engulf
        (df["Open"] > df["PrevClose"])

        &

        (df["Close"] < df["PrevOpen"])

    )

    return df
def add_swing_high(df):

    df["SwingHigh"] = (

        df["High"]
        .rolling(5)
        .max()
        .shift(1)

    )

    return df
def add_swing_low(df):

    df["SwingLow"] = (

        df["Low"]
        .rolling(5)
        .min()
        .shift(1)

    )

    return df
def add_break_swing_high(df):

    df["BreakSwingHigh"] = (

        df["Close"] >
        df["SwingHigh"]

    )

    return df
def add_break_swing_low(df):

    df["BreakSwingLow"] = (

        df["Close"] <
        df["SwingLow"]

    )

    return df
def apply_entries(df):

    df = add_bullish_engulfing(df)

    df = add_bearish_engulfing(df)

    df = add_swing_high(df)

    df = add_swing_low(df)

    df = add_break_swing_high(df)

    df = add_break_swing_low(df)

    return df