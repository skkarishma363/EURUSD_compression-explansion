def clean_data(df):

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove missing values
    df = df.dropna()

    return df