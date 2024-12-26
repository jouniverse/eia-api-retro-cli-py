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


def petroleumCrudeOilProduction():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "petroleum/crd/crpdn/"

    # Get available time range
    url_time = URL_BASE + endpoint
    res_time = requests.get(url_time, params={"api_key": API_KEY})
    data_time = res_time.json()
    end_time = datetime.strptime(data_time["response"]["endPeriod"], "%Y-%m")
    end_month = end_time.strftime("%Y-%m")
    # start is 6 months before end_time
    start_time = end_time - relativedelta(months=6)
    start_month = start_time.strftime("%Y-%m")

    # Get data
    url = URL_BASE + endpoint + "data"

    # EPC0 = Crude Oil
    # EPCANS = ANS Crude Oil
    products = ["EPC0"]
    product_labels = ["Crude Oil"]
    regions = ["R10", "R20", "R30", "R40", "R50"]
    region_labels = {
        "R10": "PADD1",
        "R20": "PADD2",
        "R30": "PADD3",
        "R40": "PADD4",
        "R50": "PADD5",
    }

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[product][]": products,
        "facets[duoarea][]": regions,
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

    #  remove items fro the column units where the value is "MBBL/D"
    df = df[df["units"] != "MBBL/D"]
    df["value"] = pd.to_numeric(df["value"])

    #  sort df by period into ascending order
    df = df.sort_values(by="period")

    #  save df to csv
    df.to_csv(
        f"./output/petroleum_crude_oil_production_{start_time.strftime('%Y-%m')}-{end_time.strftime('%Y-%m')}.csv",
        index=False,
    )

    mean_production = {}
    for product in products:
        product_data = df[df["product"] == product]
        mean_production[product] = product_data["value"].mean()

    table_data = []
    for product in products:
        for region in regions:
            product_data = df[(df["product"] == product) & (df["duoarea"] == region)]
            mean_production = product_data["value"].mean()
            table_data.append([product, region_labels[region], region, mean_production])

    print("-" * 15)
    print(
        f"Mean crude oil production {start_time.strftime('%Y-%m')}-{end_time.strftime('%Y-%m')} (1000 bbl/month)"
    )
    print(
        tabulate(
            table_data,
            headers=["Product", "Region Name", "Region", "Mean Production"],
            tablefmt="grid",
        )
    )

    # Ensure the period column is in datetime format
    df["period"] = pd.to_datetime(df["period"])

    # #  plot a time series of the production for each product
    plt.clear_figure()
    plt.date_form("Y-m")
    for region in regions:
        region_data = df[df["duoarea"] == region]
        x_values = region_data["period"].dt.strftime("%Y-%m")
        plt.plot(x_values, region_data["value"], label=region)
    plt.ylabel("1000 bbl/month")
    plt.title(
        f"Crude oil production {start_time.strftime('%Y-%m')}-{end_time.strftime('%Y-%m')} (1000 bbl/month)"
    )
    plt.theme("pro")
    plt.show()


if __name__ == "__main__":
    petroleumCrudeOilProduction()
