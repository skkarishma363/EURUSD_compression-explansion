import pandas as pd
import glob
import os


def load_forex_data(data_folder):

    # Find all CSV files
    csv_files = glob.glob(
        os.path.join(data_folder, "*.csv")
    )

    dataframes = []

    for file in csv_files:

        print(f"Loading: {file}")

        # Read CSV
        df = pd.read_csv(file)

        # Assign columns
        df.columns = [
            "Date",
            "Time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]

        # Create datetime column
        df["DateTime"] = pd.to_datetime(
            df["Date"] + " " + df["Time"]
        )

        # Set index
        df.set_index("DateTime", inplace=True)

        # Keep only OHLCV
        df = df[
            [
                "Open",
                "High",
                "Low",
                "Close",
                "Volume"
            ]
        ]

        dataframes.append(df)

    # Merge all years
    combined_df = pd.concat(dataframes)

    # Remove duplicates
    combined_df = combined_df[
        ~combined_df.index.duplicated()
    ]

    # Sort by datetime
    combined_df.sort_index(inplace=True)

    print("\nData Loaded Successfully!")

    return combined_df