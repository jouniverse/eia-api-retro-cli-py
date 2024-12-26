import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY

#  facets[duoarea][] = ["SCA","STX","SNY","SFL"]
#  California, Texas, New York, Florida


def naturalGasPriceTrends():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "natural-gas/pri/sum/"

    # Get available time range
    url_time = URL_BASE + endpoint
    res_time = requests.get(url_time, params={"api_key": API_KEY})
    data_time = res_time.json()

    # Start time = first year %Y, end year = last year %Y
    start_time = datetime.strptime(data_time["response"]["startPeriod"], "%Y-%m")
    start_year = start_time.strftime("%Y")
    end_time = datetime.strptime(data_time["response"]["endPeriod"], "%Y-%m")
    end_year = end_time.strftime("%Y")

    # Get data
    url = URL_BASE + endpoint + "data"

    # Price Delivered to Residential Consumers
    process = ["PRS"]

    regions = ["SCA", "STX", "SNY", "SFL", "SWA"]
    # regions = ["SCA"]

    region_labels = {
        "SCA": "CALIFORNIA",
        "STX": "TEXAS",
        "SNY": "NEW YORK",
        "SFL": "FLORIDA",
        "SWA": "WASHINGTON",
    }
    # region_labels = {"SCA": "CALIFORNIA"}

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "frequency": "annual",
        "facets[process][]": process,
        "facets[duoarea][]": regions,
        "start": start_year,
        "end": end_year,
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

    df["value"] = pd.to_numeric(df["value"])

    df = df.sort_values(by="period")

    #  save df to csv
    df.to_csv(
        f"./output/natural_gas_price_delivered_to_residential_consumers_{start_year}-{end_year}.csv",
        index=False,
    )

    table_data = []
    for region in regions:
        region_data = df[df["duoarea"] == region].copy()

        if len(region_data) == 0:
            print(f"Warning: No data available for {region_labels[region]}")
            continue

        # Filter out null values
        region_data = region_data.dropna(subset=["value"])

        if len(region_data) == 0:
            print(f"Warning: No non-null data available for {region_labels[region]}")
            continue

        # Sort by period and print first few rows to debug
        region_data = region_data.sort_values("period")
        print(f"\nDebug for {region_labels[region]}:")
        print(region_data[["period", "value"]].head())

        # Get first non-null row
        first_row = region_data.iloc[0]
        first_value = first_row["value"]
        first_year = first_row["period"]

        # Get last non-null row
        last_row = region_data.iloc[-1]
        last_value = last_row["value"]
        last_year = last_row["period"]

        difference = last_value - first_value

        # Format the values with years in brackets
        first_cell = f"{first_value:.2f} ({first_year})"
        last_cell = f"{last_value:.2f} ({last_year})"

        table_data.append(
            [region_labels[region], first_cell, last_cell, f"{difference:.2f}"]
        )

    if len(table_data) > 0:
        print("-" * 100)
        print("Gas Delivered to Residential Consumers ($/MCF):")
        print(
            tabulate(
                table_data,
                headers=["Region", "First Value", "Last Value", "Difference"],
                tablefmt="grid",
            )
        )
    else:
        print("No data available for comparison")

    df["period"] = pd.to_datetime(df["period"])

    plt.clear_figure()
    plt.plotsize(300, 50)
    plt.date_form("Y")

    for region in regions:
        region_data = df[df["duoarea"] == region]
        x_values = region_data["period"].dt.strftime("%Y")
        plt.plot(x_values, region_data["value"], label=region_labels[region])

    plt.title(
        f"Natural Gas Price Trends {start_year}-{end_year} - Gas Delivered to Residential Consumers"
    )
    plt.ylabel("$/MCF")
    plt.theme("pro")
    plt.show()


if __name__ == "__main__":
    naturalGasPriceTrends()
