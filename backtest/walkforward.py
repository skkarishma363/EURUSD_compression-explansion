import pandas as pd

from backtest.engine import (
    run_synchronized_backtest
)

from backtest.metrics import (
    calculate_metrics
)
def run_walk_forward_tests(

    sync_trades,

    df_m5

):

    print("\n===== WALK FORWARD TESTS =====")

    # =========================
    # DEFINE TEST WINDOWS
    # =========================

    test_periods = [

        ("2023-01-01", "2023-12-31"),

        ("2024-01-01", "2024-12-31"),

        ("2025-01-01", "2025-12-31")

    ]

    # =========================
    # LOOP THROUGH PERIODS
    # =========================

    for start_date, end_date in test_periods:

        print("\n---------------------------")
        print(f"TEST PERIOD:")
        print(f"{start_date} → {end_date}")

        # =========================
        # FILTER TRADES
        # =========================

        filtered_trades = sync_trades[

            (
                sync_trades["EntryTime"]
                >=
                start_date
            )

            &

            (
                sync_trades["EntryTime"]
                <=
                end_date
            )

        ]

        # =========================
        # RUN BACKTEST
        # =========================

        results = run_synchronized_backtest(

            filtered_trades,

            df_m5

        )

        # =========================
        # SHOW RESULTS
        # =========================

        if len(results) == 0:

            print("No trades found.")

            continue

        calculate_metrics(results)
