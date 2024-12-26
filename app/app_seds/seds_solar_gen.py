import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def sedsSolarGeneration():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "seds/"

    # Get data
    url = URL_BASE + endpoint + "data"

    # SOTGP -> Solar thermal and photovoltaic electricity total net generation
    seriesIds = ["SOTGP"]

    seriesId_labels = {
        "SOTGP": "Solar thermal and photovoltaic electricity total net generation",
    }

    regions = ["US"]

    region_labels = {
        "US": "United States",
    }

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[seriesId][]": seriesIds,
        "facets[stateId][]": regions,
        "frequency": "annual",
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

    df = pd.DataFrame(data_all)

    # Convert value to numeric first
    df["value"] = pd.to_numeric(df["value"])

    #  sort df by period into ascending order
    df = df.sort_values(by="period")

    # Find the index of the last zero before non-zero values begin
    last_zero_idx = None
    for i in range(len(df) - 1):
        if df["value"].iloc[i] == 0 and df["value"].iloc[i + 1] > 0:
            last_zero_idx = i
            break

    # If we found a transition point, filter the DataFrame
    if last_zero_idx is not None:
        df = df.iloc[last_zero_idx:]  # Keep from last zero onwards

    # Calculate statistics for the US total
    min_val = df["value"].min()
    max_val = df["value"].max()
    range_val = max_val - min_val
    current_val = df["value"].iloc[-1]

    # Calculate growth rates
    total_years = len(df) - 1  # -1 because we're calculating change between years
    first_non_zero = (
        df["value"][df["value"] > 0].iloc[0] if (df["value"] > 0).any() else None
    )
    last_value = df["value"].iloc[-1]
    absolute_growth_rate = (max_val - min_val) / total_years  # GWH per year

    # Calculate relative growth rate only if a valid first non-zero value exists
    if first_non_zero:
        relative_growth_rate = (
            (last_value / first_non_zero) ** (1 / total_years) - 1
        ) * 100  # % per year
        relative_growth_str = f"{relative_growth_rate:.2f}%"
    else:
        relative_growth_str = "N/A"  # Or "undefined"

    # Create table with US totals including growth rates
    table_data = [
        [
            "US",
            "United States",
            min_val,
            max_val,
            range_val,
            current_val,
            f"{absolute_growth_rate:.2f}",
            relative_growth_str,
        ]
    ]

    if len(table_data) > 0:
        first_period = pd.to_datetime(df["period"].min()).strftime("%Y")
        end_period = pd.to_datetime(df["period"].max()).strftime("%Y")

        #  save df to csv
        df.to_csv(
            f"./output/seds_solar_generation_{first_period}-{end_period}.csv",
            index=False,
        )

        print("-" * 100)
        print(f"Total US Solar Generation {first_period}-{end_period} (GWH):")
        print(
            tabulate(
                table_data,
                headers=[
                    "ID",
                    "Region",
                    "Min",
                    "Max",
                    "Range",
                    f"Current ({end_period})",
                    "Avg Growth (GWH/year)",
                    "Avg Growth (%/year)",
                ],
                tablefmt="grid",
            )
        )

    # Plot total US generation over time
    plt.clear_figure()
    plt.date_form("Y")
    plt.plot(
        pd.to_datetime(df["period"]).dt.strftime("%Y"),
        df["value"],
        label="Total US Solar Generation",
    )
    plt.title(f"Total US Solar Generation {first_period}-{end_period} (GWH)")
    plt.ylabel("GWH")
    plt.theme("pro")
    plt.show()


if __name__ == "__main__":
    sedsSolarGeneration()
