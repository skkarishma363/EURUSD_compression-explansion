import pandas as pd
import numpy as np
import ta
def add_body_size(df):

    df["BodySize"] = abs(
        df["Close"] - df["Open"]
    )

    return df
def add_candle_range(df):

    df["CandleRange"] = (
        df["High"] - df["Low"]
    )

    return df
def add_atr(df, period=14):

    # Previous close
    df["PrevClose"] = df["Close"].shift(1)

    # True range components
    df["TR1"] = df["High"] - df["Low"]

    df["TR2"] = abs(
        df["High"] - df["PrevClose"]
    )

    df["TR3"] = abs(
        df["Low"] - df["PrevClose"]
    )

    # True range
    df["TrueRange"] = df[
        ["TR1", "TR2", "TR3"]
    ].max(axis=1)

    # ATR
    df["ATR"] = (
        df["TrueRange"]
        .rolling(period)
        .mean()
    )

    return df
def add_ema(df, period=200):

    df["EMA"] = (
        df["Close"]
        .ewm(
            span=period,
            adjust=False
        )
        .mean()
    )

    return df
def add_ema_slope(df):

    df["EMASlope"] = (
        df["EMA"] -
        df["EMA"].shift(1)
    )

    return df
def add_trend(df):

    conditions = [
        (
            (df["Close"] > df["EMA"]) &
            (df["EMASlope"] > 0)
        ),

        (
            (df["Close"] < df["EMA"]) &
            (df["EMASlope"] < 0)
        )
    ]

    choices = ["BUY", "SELL"]

    df["Trend"] = np.select(
        conditions,
        choices,
        default="NO TREND"
    )

    return df
def add_bollinger_bands(
    df,
    period=20,
    std_dev=2
):

    # Middle band
    df["BB_Middle"] = (
        df["Close"]
        .rolling(period)
        .mean()
    )

    # Standard deviation
    df["BB_STD"] = (
        df["Close"]
        .rolling(period)
        .std()
    )

    # Upper band
    df["BB_Upper"] = (
        df["BB_Middle"] +
        (std_dev * df["BB_STD"])
    )

    # Lower band
    df["BB_Lower"] = (
        df["BB_Middle"] -
        (std_dev * df["BB_STD"])
    )

    # Band width
    df["BB_Width"] = (
        df["BB_Upper"] -
        df["BB_Lower"]
    )

    return df
def add_adx(df):

    # =========================
    # ADX TREND STRENGTH
    # =========================

    adx_indicator = ta.trend.ADXIndicator(

        high=df["High"],

        low=df["Low"],

        close=df["Close"],

        window=14

    )

    df["ADX"] = adx_indicator.adx()

    return df
def add_ema_distance(df):

    # =========================
    # EMA DISTANCE %
    # =========================

    df["EMADistance"] = (

        abs(

            df["Close"] -

            df["EMA"]

        )

        /

        df["EMA"]

    ) * 100

    return df
def apply_indicators(df):

    df = add_body_size(df)

    df = add_candle_range(df)

    df = add_atr(df)

    df = add_ema(df)

    df = add_ema_slope(df)

    df = add_trend(df)

    df = add_bollinger_bands(df)
    df = add_adx(df)
    df = add_ema_distance(df)
    return df
