import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def petroleumSpotPrices():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "petroleum/pri/spt/"

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

    regions = ["Y35NY", "Y05LA"]
    products = ["EPMRU", "EPMRR", "EPD2DXL0", "EPD2DC"]

    product_labels = {
        "EPMRU": "Conventional Regular Gasoline",
        "EPMRR": "Reformulated Regular Gasoline",
        "EPD2DXL0": "No 2 Diesel Low Sulfur (0-15 ppm)",
        "EPD2DC": " Carb Diesel",
    }

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[duoarea][]": regions,
        "facets[product][]": products,
        "start": start_hour,
        "end": end_hour,
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

    # df = pd.DataFrame(data_all["response"]["data"])
    df["value"] = pd.to_numeric(df["value"])

    # sort df by period into ascending order
    df = df.sort_values(by="period")

    #  save df to csv
    df.to_csv(
        f"./output/petroleum_spot_prices_{start_time.strftime('%Y-%m-%d')}-{end_time.strftime('%Y-%m-%d')}.csv",
        index=False,
    )

    # Print the average spot price for each product
    # New York: EPMRU (gasoline) and EPD2DXL0 (diesel)
    # Los Angeles: EPMRR (gasoline) and EPD2DC (diesel)
    mean_prices = {}
    current_prices = {}
    print("-" * 15)
    for product in products:
        product_data = df[df["product"] == product]
        product_price = product_data["value"].mean()
        mean_prices[product] = product_price

    for product in products:
        product_data = df[df["product"] == product]
        product_price = product_data["value"].values[0]
        current_prices[product] = product_price

    #  Make a table of the average spot prices
    table_data = [
        ["Product", "Name", "Price"],
        *[
            [product, product_labels[product], mean_prices[product]]
            for product in products
        ],
    ]
    print(
        f"Average spot price {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')} - Last 7 days(USD/gal):"
    )
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
    print("-" * 15)
    # Make a table of the current spot prices
    table_data = [
        ["Product", "Name", "Price"],
        *[
            [product, product_labels[product], current_prices[product]]
            for product in products
        ],
    ]
    print(f"Current ({end_time.strftime('%Y-%m-%d')}) spot prices (USD/gal):")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

    # Ensure the period column is in datetime format
    df["period"] = pd.to_datetime(df["period"])

    plt.clear_figure()
    plt.date_form("d/m/Y H:M")

    for product in products:
        product_data = df[df["product"] == product]
        x_values = product_data["period"].dt.strftime("%d/%m/%Y %H:%M")
        plt.plot(x_values, product_data["value"], label=product)

    plt.title(
        f"Spot prices for petroleum products {start_time.strftime('%Y-%m-%d')}-{end_time.strftime('%Y-%m-%d')}"
    )
    plt.ylabel("Price (USD/gal)")
    plt.theme("pro")
    plt.show()
