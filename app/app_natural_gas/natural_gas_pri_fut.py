import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def naturalGasGasPriceFuturesAndSpotPrices():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "natural-gas/pri/fut/"

    # Get available time range
    url_time = URL_BASE + endpoint
    res_time = requests.get(url_time, params={"api_key": API_KEY})
    data_time = res_time.json()

    end_time = datetime.strptime(data_time["response"]["endPeriod"], "%Y-%m-%d")
    end_month = end_time.strftime("%Y-%m-%d")
    # start is 1 month before end_time
    start_time = end_time - timedelta(days=30)
    start_month = start_time.strftime("%Y-%m-%d")

    # Get data
    url = URL_BASE + endpoint + "data"

    # RGC = NA, Y35NY = NEW YORK CITY
    # region = ["RGC", "Y35NY"]
    regions = ["RGC"]

    # region_labels = {
    #     "RGC": "NA",
    #     "Y35NY": "NEW YORK CITY",
    # }
    region_labels = {
        "RGC": "NA",
    }

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[duoarea][]": regions,
        "start": start_month,
        "end": end_month,
        "frequency": "daily",
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

    # sort df by period
    df = df.sort_values(by="period")

    #  save df to csv
    df.to_csv(
        f"./output/natural_gas_gas_price_futures_and_spot_prices_{start_month}-{end_month}.csv",
        index=False,
    )

    table_data = []
    for region in regions:
        region_data = df[df["duoarea"] == region]
        min_val = region_data["value"].min()
        max_val = region_data["value"].max()
        range_val = max_val - min_val
        mean_val = region_data["value"].mean()
        table_data.append(
            [region_labels[region], min_val, max_val, range_val, mean_val]
        )
    description = df["series-description"].unique()
    process_name = df["process-name"].unique()
    print("-" * 100)
    print(description[0] + ", i.e. " + process_name[0] + " Last 30 days ($/MMBTU):")
    print(
        tabulate(
            table_data,
            headers=["Region", "Min", "Max", "Range", "Mean"],
            tablefmt="grid",
        )
    )

    # Convert period to datetime first
    df["period"] = pd.to_datetime(df["period"])

    plt.clear_figure()
    # plt.plotsize(300, 50)
    plt.date_form("d/m/Y")

    average_values = {}
    for region in regions:
        region_data = df[df["duoarea"] == region]
        x_values = region_data["period"].dt.strftime("%d/%m/%Y")
        plt.plot(x_values, region_data["value"], label=region_labels[region])

    average_value = df["value"].mean()
    x_values = df["period"].dt.strftime("%d/%m/%Y")
    # Add average line to the plot
    plt.plot(
        x_values,
        [average_value] * len(x_values),
        label=f"Average: {average_value:.2f}",
        marker="dot",
    )

    plt.title(description[0] + ", i.e. " + process_name[0] + "(last 30 days):")
    plt.ylabel("$/MMBTU")
    plt.theme("pro")
    plt.show()


if __name__ == "__main__":
    naturalGasGasPriceFuturesAndSpotPrices()
