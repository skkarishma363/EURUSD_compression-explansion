def add_buy_breakout(df):

    df["BuyBreakout"] = (
        df["Close"] >
        df["RangeHigh"]
    )

    return df
def add_sell_breakout(df):

    df["SellBreakout"] = (
        df["Close"] <
        df["RangeLow"]
    )

    return df
def add_breakout_strength(df):

    # Average body size
    df["AvgBody10"] = (
        df["BodySize"]
        .rolling(10)
        .mean()
        .shift(1)
    )

    # Strong breakout candle
    df["StrongBreakout"] = (
        df["BodySize"] >
        (1.2 * df["AvgBody10"])
    )

    return df
def shift_compression(df):

    # Compression must happen BEFORE breakout
    df["PreviousCompression"] = (
        df["ValidCompression"]
        .shift(1)
    )

    return df
def add_final_buy_breakout(
    df,
    adx_threshold=25,
    ema_distance_threshold=0.15
):

    df["FinalBuyBreakout"] = (

        df["PreviousCompression"]

        &

        df["BuyBreakout"]

        &

        df["StrongBreakout"]

        &

        (df["Trend"] == "BUY")
        &
        (df["ADX"] > 25)
        &
        (df["EMADistance"] > 0.15)
    )

    return df
def add_final_sell_breakout(
    df,
    adx_threshold=25,
    ema_distance_threshold=0.15
):

    df["FinalSellBreakout"] = (

        df["PreviousCompression"]

        &

        df["SellBreakout"]

        &

        df["StrongBreakout"]

        &

        (df["Trend"] == "SELL")
        &
        (df["ADX"] > adx_threshold)
        &
        (df["EMADistance"] > ema_distance_threshold)
    )

    return df
import numpy as np


def add_breakout_direction(df):

    conditions = [
        df["FinalBuyBreakout"],
        df["FinalSellBreakout"]
    ]

    choices = ["BUY", "SELL"]

    df["BreakoutDirection"] = np.select(
        conditions,
        choices,
        default="NONE"
    )

    return df
def apply_breakouts(
    df,
    adx_threshold=25,
    ema_distance_threshold=0.15
):

    df = add_buy_breakout(df)

    df = add_sell_breakout(df)

    df = add_breakout_strength(df)

    df = shift_compression(df)

    df = add_final_buy_breakout(df, adx_threshold, ema_distance_threshold)

    df = add_final_sell_breakout(
    df,
    adx_threshold,
    ema_distance_threshold
)

    df = add_breakout_direction(df)

    return df