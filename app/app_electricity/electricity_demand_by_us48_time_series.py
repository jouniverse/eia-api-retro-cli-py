import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
import pandas as pd
from tabulate import tabulate
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY

URL_BASE = "https://api.eia.gov/v2/"


def electricityDemandUS48Last7Days():
    endpoint = "electricity/rto/region-data/"
    url = URL_BASE + endpoint + "data"

    # Get current hour in UTC
    current_time = datetime.now(UTC)
    start_time = current_time - timedelta(days=7)
    start_hour = start_time.strftime("%Y-%m-%dT%H")
    end_time = current_time - timedelta(hours=2)
    end_hour = end_time.strftime("%Y-%m-%dT%H")

    regions = ["US48"]

    facets = "D"

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[type][]": facets,
        "facets[respondent][]": regions,
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

    #  print max, min, range and avg demand for US48
    print("-" * 100)
    print(
        f"Demand US48 {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')} (last 7 days):"
    )
    us48_data = df[df["respondent"] == "US48"]
    table_data = [
        ["Max", f"{us48_data['value'].max():,.0f} MWh"],
        ["Min", f"{us48_data['value'].min():,.0f} MWh"],
        ["Range", f"{us48_data['value'].max() - us48_data['value'].min():,.0f} MWh"],
        ["Avg", f"{us48_data['value'].mean():,.0f} MWh"],
    ]
    print(tabulate(table_data, headers=["Statistic", "Value"], tablefmt="grid"))

    # export df to csv
    df.to_csv(
        f"./output/electricity_demand_by_us48_time_series_{current_time.strftime('%Y-%m-%d')}.csv",
        index=False,
    )

    # Ensure the period column is in datetime format
    df["period"] = pd.to_datetime(df["period"])

    # Plot a time series of the demand by region
    plt.clear_figure()

    plt.date_form("d/m/Y H:M")  # Set the date format

    for region in regions:
        region_data = df[df["respondent"] == region]
        # Format datetime to dd/mm/yyyy HH:MM
        x_values = region_data["period"].dt.strftime("%d/%m/%Y %H:%M")
        plt.plot(x_values, region_data["value"], label=region)

    plt.title("Electricity Demand US48 - Last 7 Days")
    plt.ylabel("MWh")
    plt.theme("pro")

    average_value = df["value"].mean()
    region_data = df[df["respondent"] == "US48"]
    x_values = region_data["period"].dt.strftime("%d/%m/%Y %H:%M")
    plt.plot(
        x_values,
        [average_value] * len(x_values),
        label=f"Average: {average_value:.2f} MWh",
        marker="dot",
    )
    plt.show()


if __name__ == "__main__":
    electricityDemandUS48Last7Days()
