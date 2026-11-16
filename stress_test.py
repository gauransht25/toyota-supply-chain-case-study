"""Evaluate stand-alone part exposure for an illustrative supply interruption."""

import csv
from pathlib import Path


def uncovered_days(stock, daily_usage, recovery_days):
    if daily_usage <= 0 or min(stock, recovery_days) < 0:
        raise ValueError("Daily usage must be positive and stock and recovery nonnegative.")
    return max(0, recovery_days - stock / daily_usage)


def main():
    columns = ("part", "coverage_days", "base_gap_days", "severe_gap_days", "mitigated_gap_days")
    print(",".join(columns))
    with Path(__file__).with_name("parts.csv").open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            stock, usage = int(row["usable_stock"]), int(row["daily_usage"])
            base = uncovered_days(stock, usage, int(row["base_recovery"]))
            severe = uncovered_days(stock, usage, int(row["severe_recovery"]))
            mitigated = uncovered_days(
                stock + int(row["extra_stock"]), usage, int(row["mitigated_severe_recovery"])
            )
            print(f"{row['part']},{stock / usage:.1f},{base:.1f},{severe:.1f},{mitigated:.1f}")


if __name__ == "__main__":
    main()
