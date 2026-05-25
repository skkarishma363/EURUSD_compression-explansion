def add_session_filter(df):

    # Extract hour
    df["Hour"] = df.index.hour

    # Extract weekday
    df["Weekday"] = df.index.weekday

    # =========================
    # London Session
    # =========================

    london_session = (

        (df["Hour"] >= 7)

        &

        (df["Hour"] <= 16)

    )

    # =========================
    # Friday Filter
    # =========================

    friday_late = (

        (df["Weekday"] == 4)

        &

        (df["Hour"] >= 17)

    )

    # =========================
    # Final Trading Session
    # =========================

    df["ValidSession"] = (

        london_session

        &

        (~friday_late)

    )

    return df
