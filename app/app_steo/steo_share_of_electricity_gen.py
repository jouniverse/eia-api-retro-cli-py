import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def steoSharesOfUSElectricityGeneration():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "steo/"

    # Get data
    url = URL_BASE + endpoint + "data"

    # region = U.S.
    seriesIds = ["CLEPSHR_US", "NGEPSHR_US", "NUEPSHR_US", "RTEPSHR_US"]

    series_labels = {
        "CLEPSHR_US": "Coal",
        "NGEPSHR_US": "Natural Gas",
        "NUEPSHR_US": "Nuclear",
        "RTEPSHR_US": "Renewables",
    }

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[seriesId][]": seriesIds,
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
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Order df by column period into ascending order before plotting
    df = df.sort_values(by="period")

    first_period = pd.to_datetime(df["period"].min()).strftime("%Y")
    end_period = pd.to_datetime(df["period"].max()).strftime("%Y")

    #  save df to csv
    df.to_csv(
        f"./output/shares_of_us_electricity_generation_{first_period}-{end_period}.csv",
        index=False,
    )

    table_data = []
    for idx in seriesIds:
        facet_data = df[df["seriesId"] == idx]
        # Drop NaN values after getting the facet data
        facet_data = facet_data.dropna(subset=["value"])

        if len(facet_data) == 0:
            print(f"Warning: No valid data for sector {series_labels[idx]}")
            continue

        min_val = facet_data["value"].min()
        max_val = facet_data["value"].max()
        range_val = max_val - min_val
        current_val = facet_data["value"].iloc[-1]

        table_data.append(
            [idx, series_labels[idx], min_val, max_val, range_val, current_val]
        )

    if len(table_data) > 0:
        # first_period = pd.to_datetime(df["period"].min()).strftime("%Y")
        # end_period = pd.to_datetime(df["period"].max()).strftime("%Y")

        print("-" * 100)
        print(f"Shares of U.S. Electricity Generation {first_period}-{end_period} (%)")
        print(
            tabulate(
                table_data,
                headers=[
                    "ID",
                    "Name",
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

    for idx in seriesIds:
        facet_data = df[df["seriesId"] == idx]
        if len(facet_data) > 0:  # Only plot if we have data
            x_values = facet_data["period"].dt.strftime("%Y")
            plt.plot(x_values, facet_data["value"], label=series_labels[idx])

    plt.title(f"Shares of U.S. Electricity Generation {first_period}-{end_period} (%)")
    plt.ylabel("Share of Total Generation (%)")
    plt.theme("pro")

    plt.show()


if __name__ == "__main__":
    steoSharesOfUSElectricityGeneration()
