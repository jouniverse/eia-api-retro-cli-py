import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def naturalGasPriceSummary():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "natural-gas/pri/sum/"

    # Get available time range
    url_time = URL_BASE + endpoint
    res_time = requests.get(url_time, params={"api_key": API_KEY})
    data_time = res_time.json()

    end_time = datetime.strptime(data_time["response"]["endPeriod"], "%Y-%m")
    end_month = end_time.strftime("%Y-%m")
    # start is 1 month before end_time
    start_time = end_time - timedelta(days=30)
    start_month = start_time.strftime("%Y-%m")

    #  Get data
    url = URL_BASE + endpoint + "data"

    process = [
        "PCS",
        "PEU",
        "PEX",
        "PG1",
        "PIN",
        "PM0",
        "PML",
        "PNG",
        "PNP",
        "PRP",
        "PRS",
    ]

    process_labels = {
        "PCS": "Price Delivered to Commercial Sectors",
        "PEU": "Electric Power Price",
        "PEX": "Exports (Price)",
        "PG1": "City Gate Price",
        "PIN": "Industrial Price",
        "PM0": "Imports Price",
        "PML": "LNG Imports (Price) (",
        "PNG": "Liquefied Natural Gas Exports Price",
        "PNP": "Pipeline Exports (Price)",
        "PRP": "Pipeline Imports Price",
        "PRS": "Price Delivered to Residential Consumers",
    }

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[process][]": process,
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

    df = pd.DataFrame(data_all)
    df["value"] = pd.to_numeric(df["value"])

    #  save df to csv
    #  current time -> only year and month
    current_time = datetime.now().strftime("%Y-%m")
    df.to_csv(
        f"./output/natural_gas_price_delivered_to_commercial_sectors_{current_time}.csv",
        index=False,
    )

    # Prepare data for plotting
    box_data = []
    process_order = []
    mean_prices = {}  # Initialize the dictionary here

    for process_id in process:
        process_df = df[df["process"] == process_id]
        values = process_df["value"]

        # Calculate statistics for box plot
        max_val = values.max()
        q75 = values.quantile(0.75)
        q50 = values.median()
        q25 = values.quantile(0.25)
        min_val = values.min()

        box_data.append([max_val, q75, q50, q25, min_val])
        process_order.append(process_id)
        mean_prices[process_id] = values.mean()

    # Sort by mean values
    sorted_items = sorted(mean_prices.items(), key=lambda x: x[1], reverse=True)
    process_order = [item[0] for item in sorted_items]
    box_data = [box_data[process.index(proc)] for proc in process_order]

    # Print table as before
    table_data = [
        ["Process", "Process Name", "Min", "Max", "Range", "Mean"],
        *[
            [
                process,
                process_labels[process],
                df[df["process"] == process]["value"].min(),
                df[df["process"] == process]["value"].max(),
                df[df["process"] == process]["value"].max()
                - df[df["process"] == process]["value"].min(),
                df[df["process"] == process]["value"].mean(),
            ]
            for process in process
        ],
    ]
    print("-" * 100)
    print(
        f"Natural gas price summary - last available data {end_time.strftime('%Y-%m')} ($/MCF)"
    )
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

    # Create box plot
    plt.clear_figure()

    # Draw box plot
    plt.box(process_order, box_data, width=0.3, quintuples=True)

    # Add mean line
    average_value = sum(mean_prices.values()) / len(mean_prices)
    plt.plot(
        [average_value] * len(process_order),
        label=f"Average: {average_value:.2f}",
        marker="dot",
    )

    plt.title(
        f"Natural Gas Price Distribution ($/MCF) - Last Available Data {end_time.strftime('%Y-%m')}"
    )
    plt.ylabel("$/MCF")
    plt.theme("pro")
    plt.show()


if __name__ == "__main__":
    naturalGasPriceSummary()
