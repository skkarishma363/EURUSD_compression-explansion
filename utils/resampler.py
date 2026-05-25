def resample_timeframes(df):

    # M5 candles
    df_m5 = df.resample("5min").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    })

    # H1 candles
    df_h1 = df.resample("1h").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    })

    # Remove empty candles
    df_m5.dropna(inplace=True)
    df_h1.dropna(inplace=True)

    return df_m5, df_h1