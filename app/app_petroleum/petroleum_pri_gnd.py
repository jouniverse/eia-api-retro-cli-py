import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def petroleumWeeklyRetailGasolineAndDieselPrices():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "petroleum/pri/gnd/"

    # Get available time range
    url_time = URL_BASE + endpoint
    res_time = requests.get(url_time, params={"api_key": API_KEY})
    data_time = res_time.json()

    end_time = datetime.strptime(data_time["response"]["endPeriod"], "%Y-%m-%d")
    end_hour = end_time.strftime("%Y-%m-%dT%H")
    # start is 7 days before end_time
    start_time = end_time - timedelta(days=7)
    start_hour = start_time.strftime("%Y-%m-%dT%H")

    # Get data
    url = URL_BASE + endpoint + "data"

    products = ["EPMRU", "EPMRR", "EPD2DXL0"]
    product_labels = [
        "Conventional Regular Gasoline",
        "Reformulated Regular Gasoline",
        "No 2 Diesel Low Sulfur",
    ]

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[product][]": products,
        "start": end_hour,
        "end": end_hour,
        "frequency": "weekly",
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

    #  sort df by period into ascending order
    df = df.sort_values(by="period")

    #  save df to csv
    df.to_csv(
        f"./output/petroleum_weekly_retail_gasoline_and_diesel_prices_{end_time.strftime('%Y-%m-%d')}.csv",
        index=False,
    )

    # Print the gnd price stats for each product
    # EPMRU (gasoline) and EPD2DXL0 (diesel)
    # EPMRR (gasoline) and EPD2DC (diesel)
    mean_prices = {}
    max_prices = {}
    min_prices = {}
    range_prices = {}
    current_prices = {}
    product_names = {}
    for product in products:
        product_data = df[df["product"] == product]
        mean_prices[product] = product_data["value"].mean()
        max_prices[product] = product_data["value"].max()
        min_prices[product] = product_data["value"].min()
        range_prices[product] = (
            product_data["value"].max() - product_data["value"].min()
        )
        product_names[product] = product_labels[products.index(product)]
    print("-" * 15)
    print(
        f"Current ({end_time.strftime('%Y-%m-%d')}) weekly retail price stats  (USD/gal)"
    )
    table_data = [
        ["Product", "Name", "Min", "Max", "Mean", "Range"],
        *[
            [
                product,
                product_names[product],
                min_prices[product],
                max_prices[product],
                mean_prices[product],
                range_prices[product],
            ]
            for product in products
        ],
    ]
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

    # Prepare data for box plot
    box_data = []
    for product in products:
        product_df = df[df["product"] == product]
        values = product_df["value"]

        # Calculate statistics for box plot
        max_val = values.max()
        q75 = values.quantile(0.75)
        q50 = values.median()
        q25 = values.quantile(0.25)
        min_val = values.min()

        box_data.append([max_val, q75, q50, q25, min_val])

    # Create box plot
    plt.clear_figure()
    plt.box(products, box_data, width=0.3, quintuples=True)
    plt.title(
        f"Current ({end_time.strftime('%Y-%m-%d')}) weekly retail prices (USD/gal)"
    )
    plt.ylabel("Price (USD/gal)")
    plt.theme("pro")
    plt.show()


if __name__ == "__main__":
    petroleumWeeklyRetailGasolineAndDieselPrices()
