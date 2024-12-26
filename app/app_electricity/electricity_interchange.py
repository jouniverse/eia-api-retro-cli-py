import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
import pandas as pd
from tabulate import tabulate
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def electricityInterchangeLast7Days():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "electricity/rto/interchange-data/"
    url = URL_BASE + endpoint + "data"

    # Get current hour in UTC
    current_time = datetime.now(UTC)
    start_time = current_time - timedelta(days=7)
    start_hour = start_time.strftime("%Y-%m-%dT%H")
    end_time = current_time - timedelta(hours=2)
    end_hour = end_time.strftime("%Y-%m-%dT%H")

    regions = "US48"

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[fromba][]": regions,
        "start": start_hour,
        "end": end_hour,
        "frequency": "hourly",
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

    toba = ["MEX", "CAN"]
    fromba = "US48"  # US48 is the region of the US Lower 48 states
    print("-" * 100)
    print(
        f"Electricity Interchange between US48 and Mexico and Canada {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')} (last 7 days):"
    )
    table_data = []
    for region in toba:
        region_data = df[(df["fromba"] == fromba) & (df["toba"] == region)]
        min_value = region_data["value"].min()
        max_value = region_data["value"].max()
        range_value = max_value - min_value
        avg_value = region_data["value"].mean()
        table_data.append(
            [
                region,
                f"{min_value:.0f} MWh",
                f"{max_value:.0f} MWh",
                f"{range_value:.0f} MWh",
                f"{avg_value:.0f} MWh",
            ]
        )
    print(
        tabulate(
            table_data,
            headers=["Region", "Min", "Max", "Range", "Average"],
            tablefmt="grid",
        )
    )

    # export df to csv
    df.to_csv(
        f"./output/electricity_interchange_{toba[0]}_{toba[1]}_{current_time.strftime('%Y-%m-%d')}.csv",
        index=False,
    )

    # Ensure the period column is in datetime format
    df["period"] = pd.to_datetime(df["period"])

    plt.clear_figure()  # Clear any existing plots
    plt.date_form("d/m/Y H:M")  # Set the date format

    # Filter data for "CAN" and "MEX"
    toba = ["CAN", "MEX"]
    fromba = "US48"

    for region in toba:
        region_data = df[(df["fromba"] == fromba) & (df["toba"] == region)]
        x_values = region_data["period"].dt.strftime("%d/%m/%Y %H:%M")
        plt.plot(x_values, region_data["value"], label=region)

    plt.title(
        f"Electricity Interchange between US48 and Canada/Mexico {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')} (last 7 days)"
    )
    plt.ylabel("MWh")
    plt.theme("pro")

    plt.show()


if __name__ == "__main__":
    electricityInterchangeLast7Days()
