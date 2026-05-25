import numpy as np
def add_atr_compression(df):

    # Average ATR of last 30 candles
    df["ATR30Avg"] = (
        df["ATR"]
        .rolling(30)
        .mean()
    )

    # 70% threshold
    df["ATRThreshold"] = (
        df["ATR30Avg"] * 0.70
    )

    # Compression condition
    df["ATRCompression"] = (
        df["ATR"] <
        df["ATRThreshold"]
    )

    return df
def add_bb_compression(df):

    # Lowest 20% BB width
    threshold = (
        df["BB_Width"]
        .rolling(50)
        .quantile(0.20)
    )

    # Compression condition
    df["BBCompression"] = (
        df["BB_Width"] <
        threshold
    )

    return df
def add_overlap_compression(df):

    # Previous candle high/low
    df["PrevHigh"] = (
        df["High"].shift(1)
    )

    df["PrevLow"] = (
        df["Low"].shift(1)
    )

    # Overlap area
    df["OverlapHigh"] = df[
        ["Low", "PrevLow"]
    ].max(axis=1)

    df["OverlapLow"] = df[
        ["High", "PrevHigh"]
    ].min(axis=1)

    # Overlap size
    df["OverlapSize"] = (
        df["OverlapLow"] -
        df["OverlapHigh"]
    )

    # Overlap percentage
    df["OverlapPercent"] = (
        df["OverlapSize"] /
        df["CandleRange"]
    ) * 100

    # Condition
    df["OverlapCondition"] = (
        df["OverlapPercent"] > 50
    )

    # Count overlaps
    df["OverlapCount"] = (
        df["OverlapCondition"]
        .rolling(12)
        .sum()
    )

    # Final overlap compression
    df["OverlapCompression"] = (
        df["OverlapCount"] >= 8
    )

    return df
def add_final_compression(df):

    df["FinalCompression"] = (
        df["ATRCompression"]
        &
        df["BBCompression"]
        &
        df["OverlapCompression"]
    )

    return df
def add_compression_range(df):

    # IMPORTANT:
    # shift(1) prevents future leakage

    df["RangeHigh"] = (
        df["High"]
        .rolling(12)
        .max()
        .shift(1)
    )

    df["RangeLow"] = (
        df["Low"]
        .rolling(12)
        .min()
        .shift(1)
    )

    # Range size
    df["RangeSize"] = (
        df["RangeHigh"] -
        df["RangeLow"]
    )

    # Convert to pips
    df["RangePips"] = (
        df["RangeSize"] * 10000
    )

    # Valid range
    df["ValidRange"] = (
        (df["RangePips"] >= 10)
        &
        (df["RangePips"] <= 60)
    )

    return df
def add_valid_compression(df):

    df["ValidCompression"] = (
        df["FinalCompression"]
        &
        df["ValidRange"]
    )

    return df
def apply_compression(df):

    df = add_atr_compression(df)

    df = add_bb_compression(df)

    df = add_overlap_compression(df)

    df = add_final_compression(df)

    df = add_compression_range(df)

    df = add_valid_compression(df)

    return df
