import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def coalConsumptionAndQualityPrice():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "coal/consumption-and-quality/"

    # Get data
    url = URL_BASE + endpoint + "data"

    # region = U.S.
    locations = ["US"]

    location_labels = {
        "US": "U.S.",
    }

    sectors = ["1", "10", "2", "3", "8", "9", "94", "98"]

    sector_labels = {
        "1": "Electric Utility",
        "10": "Other Industrial",
        "2": "IPP Non-CHP",
        "3": "IPP CHP",
        "8": "Commercial and Institutional",
        "9": "Coke Plants",
        "94": "Independent Power Producers",
        "98": "Electric Power",
    }

    datasets = ["consumption", "price"]

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "price",
        "facets[location][]": locations,
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

    #  Convert price to numeric first
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Filter out sectors "2" and "3"
    df = df[~df["sector"].isin(["2", "3"])].copy()

    # Order df by column period into ascending order before plotting
    df = df.sort_values(by="period")

    first_period = pd.to_datetime(df["period"].min()).strftime("%Y")
    end_period = pd.to_datetime(df["period"].max()).strftime("%Y")

    #  save df to csv
    df.to_csv(
        f"./output/coal_consumption_and_quality_price_{first_period}-{end_period}.csv",
        index=False,
    )

    table_data = []
    for idx in sectors:
        # Skip sectors 2 and 3 in the loop as well
        if idx in ["2", "3"]:
            continue

        facet_data = df[df["sector"] == idx]
        # Drop NaN values after getting the facet data
        facet_data = facet_data.dropna(subset=["price"])

        if len(facet_data) == 0:
            print(f"Warning: No valid price data for sector {sector_labels[idx]}")
            continue

        min_val = facet_data["price"].min()
        max_val = facet_data["price"].max()
        range_val = max_val - min_val
        current_val = facet_data["price"].iloc[-1]

        table_data.append(
            [idx, sector_labels[idx], min_val, max_val, range_val, current_val]
        )

    if len(table_data) > 0:
        # first_period = pd.to_datetime(df["period"].min()).strftime("%Y")
        # end_period = pd.to_datetime(df["period"].max()).strftime("%Y")

        print("-" * 100)
        print(f"Coal Price {first_period}-{end_period} (USD/SHORT TON):")
        print(
            tabulate(
                table_data,
                headers=[
                    "Sector",
                    "Sector Label",
                    "Min",
                    "Max",
                    "Range",
                    f"Current ({end_period})",
                ],
                tablefmt="grid",
            )
        )
    else:
        print("No data available for any sector")

    # Create an explicit copy
    df["period"] = pd.to_datetime(df["period"])

    plt.clear_figure()

    plt.date_form("Y")

    for idx in sectors:
        # Skip sectors 2 and 3 in plotting as well
        if idx in ["2", "3"]:
            continue

        facet_data = df[df["sector"] == idx]
        if len(facet_data) > 0:  # Only plot if we have data
            x_values = facet_data["period"].dt.strftime("%Y")
            plt.plot(x_values, facet_data["price"], label=sector_labels[idx])

    plt.title(f"Coal Price {first_period}-{end_period} (USD/SHORT TON)")
    plt.ylabel("USD/SHORT TON")
    plt.theme("pro")

    plt.show()
