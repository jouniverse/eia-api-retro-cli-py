import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY
from dateutil.relativedelta import relativedelta


def totalEnergyMonthly():
    URL_BASE = "https://api.eia.gov/v2/"
    endpoint = "total-energy/"

    # Get available time range
    end_month = datetime.now().strftime("%Y-%m")
    start_month = (
        datetime.strptime(end_month, "%Y-%m") - relativedelta(months=3)
    ).strftime("%Y-%m")

    # Get data
    url = URL_BASE + endpoint + "data"
    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "start": start_month,
        "end": end_month,
        "frequency": "monthly",
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
    }

    data_all = []

    while True:
        res = requests.get(url, params=parameters)
        data = res.json()
        data_all.extend(data["response"]["data"])

        if len(data["response"]["data"]) < 5000:
            break

        parameters["offset"] += 5000

    # Convert to DataFrame
    df = pd.DataFrame(data_all)

    # Convert value column to numeric
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Get the most recent value for each unique series
    # First, sort by period to ensure we get the latest data
    df = df.sort_values("period", ascending=True)

    # Group by series description and get last (most recent) value for each
    latest_values = df.groupby("seriesDescription").last().reset_index()

    # Sort by series description for consistent output
    latest_values = latest_values.sort_values("seriesDescription")

    # save to csv
    latest_values.to_csv(
        f"./output/total_energy_{end_month}.csv",
        index=False,
    )
    print("-" * 100)
    print(f"Saved to csv: ./output/total_energy_{end_month}.csv")

    # # Create a vertical-style table for better readability
    # lines = []
    # separator = "-" * 80  # Separator line between records

    # for _, row in latest_values.iterrows():
    #     lines.append(separator)
    #     lines.append(f"Description: {row['seriesDescription']}")
    #     lines.append(f"Period: {row['period']}")
    #     lines.append(f"Value: {row['value']}")
    #     lines.append(f"Unit: {row['unit']}")
    # lines.append(separator)

    # # Join the lines into a single string for output
    # table = "\n".join(lines)

    # # Print the table
    # print(f"\nEnergy Data Summary (Latest Values)")
    # print(table)

    # Print summary statistics
    print("-" * 100)
    print(f"Total unique series found: {len(latest_values)}")
    print(f"Date range: {start_month} to {end_month}")
    print("- -" * 20)


if __name__ == "__main__":
    totalEnergyMonthly()
