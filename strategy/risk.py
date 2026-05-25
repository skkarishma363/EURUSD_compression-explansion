def add_buy_stop_loss(df):

    # ATR stop distance
    df["BuyATR_SL"] = (
        df["ATR"] * 1.2
    )

    # Breakout range stop
    df["BuyRange_SL"] = (
        df["Close"] -
        df["RangeLow"]
    )

    # Use larger stop
    df["BuySLDistance"] = df[
        [
            "BuyATR_SL",
            "BuyRange_SL"
        ]
    ].max(axis=1)

    # Final SL price
    df["BuySL"] = (
        df["Close"] -
        df["BuySLDistance"]
    )

    return df
def add_sell_stop_loss(df):

    # ATR stop
    df["SellATR_SL"] = (
        df["ATR"] * 1.2
    )

    # Breakout range stop
    df["SellRange_SL"] = (
        df["RangeHigh"] -
        df["Close"]
    )

    # Larger stop
    df["SellSLDistance"] = df[
        [
            "SellATR_SL",
            "SellRange_SL"
        ]
    ].max(axis=1)

    # Final SL
    df["SellSL"] = (
        df["Close"] +
        df["SellSLDistance"]
    )

    return df
def calculate_risk(df):

    # Buy risk
    df["BuyRisk"] = abs(
        df["Close"] -
        df["BuySL"]
    )

    # Sell risk
    df["SellRisk"] = abs(
        df["SellSL"] -
        df["Close"]
    )

    return df
def add_take_profit_levels(df):

    # BUY TP1
    df["BuyTP1"] = (
        df["Close"] +
        df["BuyRisk"]
    )

    # BUY TP2
    df["BuyTP2"] = (
        df["Close"] +
        (2 * df["BuyRisk"])
    )

    # SELL TP1
    df["SellTP1"] = (
        df["Close"] -
        df["SellRisk"]
    )

    # SELL TP2
    df["SellTP2"] = (
        df["Close"] -
        (2 * df["SellRisk"])
    )

    return df
def apply_risk_management(df):

    df = add_buy_stop_loss(df)

    df = add_sell_stop_loss(df)

    df = calculate_risk(df)

    df = add_take_profit_levels(df)

    return df
