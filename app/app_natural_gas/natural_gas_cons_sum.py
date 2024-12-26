import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def naturalGasConsumptionByEndUse1930(
    df, facets, facet_labels, first_period, end_period
):
    table_data = []
    for facet in facets:
        facet_data = df[df["process"] == facet]
        min_val = facet_data["value"].min()
        max_val = facet_data["value"].max()
        range_val = max_val - min_val
        current_val = facet_data["value"].iloc[-1]
        mean_val = facet_data["value"].mean()
        table_data.append(
            [
                facet,
                facet_labels[facet],
                min_val,
                max_val,
                range_val,
                mean_val,
                current_val,
            ]
        )
    print("-" * 100)
    print(f"Natural Gas Consumption by End Use {first_period}-{end_period} (MMCF):")
    print(
        tabulate(
            table_data,
            headers=[
                "Facet",
                "Name",
                "Min",
                "Max",
                "Range",
                "Mean",
                f"Current ({end_period})",
            ],
            tablefmt="grid",
        )
    )

    # Convert period to datetime first
    df["period"] = pd.to_datetime(df["period"])

    plt.clear_figure()

    plt.date_form("Y")

    for facet in facets:
        facet_data = df[df["process"] == facet]
        x_values = facet_data["period"].dt.strftime("%Y")
        plt.plot(x_values, facet_data["value"], label=facet)

    plt.title(f"Natural Gas Consumption by End Use {first_period}-{end_period} (MMCF)")
    plt.ylabel("MMCF")
    plt.theme("pro")

    plt.show()


def naturalGasConsumptionByEndUse1997(
    df, facets, facet_labels, first_period, end_period
):
    table_data = []
    for facet in facets:
        facet_data = df[df["process"] == facet]
        # min_val = facet_data["value"].min()
        # max_val = facet_data["value"].max()
        # range_val = max_val - min_val
        current_val = facet_data["value"].iloc[-1]
        mean_val = facet_data["value"].mean()
        table_data.append(
            [
                facet,
                facet_labels[facet],
                mean_val,
                current_val,
            ]
        )
    print("-" * 100)
    print(f"Natural Gas Consumption by End Use {first_period}-{end_period} (MMCF):")
    print(
        tabulate(
            table_data,
            headers=[
                "Facet",
                "Name",
                "Mean",
                f"Current ({end_period})",
            ],
            tablefmt="grid",
        )
    )

    # Convert period to datetime first
    df["period"] = pd.to_datetime(df["period"])

    plt.clear_figure()

    plt.date_form("Y")

    for facet in facets:
        facet_data = df[df["process"] == facet]
        x_values = facet_data["period"].dt.strftime("%Y")
        plt.plot(x_values, facet_data["value"], label=facet)

    plt.title(f"Natural Gas Consumption by End Use {first_period}-{end_period} (MMCF)")
    plt.ylabel("MMCF")
    plt.theme("pro")

    plt.show()


def naturalGasConsumptionByEndUse():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "natural-gas/cons/sum/"
    # Get data
    url = URL_BASE + endpoint + "data"

    # region = U.S.
    regions = ["NUS"]

    region_labels = {
        "NUS": "U.S.",
    }

    # ENC, ENG, ENP, ERE, ETR, EVE, EVT
    facets = ["VCS", "VGL", "VRS"]

    #  1930 -
    facet_labels = {
        "VCS": "Commercial Consumption",
        "VGL": "Lease and Plant Fuel Consumption",
        "VRS": "Residential Consumption",
    }

    #  others ~1997-
    # facets = ["VCS", "VDV", "VEU", "VGL", "VGP", "VGT", "VIN", "VRS"]
    # facet_labels = {
    #     "VCS": "Commercial Consumption",
    #     "VDV": "Vehicle Fuel Consumption",
    #     "VEU": "Electric Power Consumption",
    #     "VGL": "Lease and Plant Fuel Consumption",
    #     "VGP": "Pipeline Fuel Consumption",
    #     "VGT": "Delivered to Consumers",
    #     "VIN": "Industrial Consumption",
    #     "VRS": "Residential Consumption",
    # }

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[duoarea][]": regions,
        "facets[process][]": facets,
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

    df["value"] = pd.to_numeric(df["value"])
    # print(df["period"])

    #  find the first period for which there is data
    first_period = pd.to_datetime(df["period"].min()).strftime("%Y")
    #  find the last period for which there is data
    end_period = pd.to_datetime(df["period"].max()).strftime("%Y")

    df_1930 = df.sort_values(by="period")

    #  save df to csv
    df_1930.to_csv(
        f"./output/natural_gas_consumption_by_end_use_{first_period}-{end_period}.csv",
        index=False,
    )

    naturalGasConsumptionByEndUse1930(
        df_1930, facets, facet_labels, first_period, end_period
    )

    #  others ~1997-
    facets = ["VDV", "VEU", "VGP", "VGT", "VIN"]
    facet_labels = {
        "VDV": "Vehicle Fuel Consumption",
        "VEU": "Electric Power Consumption",
        "VGP": "Pipeline Fuel Consumption",
        "VGT": "Delivered to Consumers",
        "VIN": "Industrial Consumption",
    }

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[duoarea][]": regions,
        "facets[process][]": facets,
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

    df["value"] = pd.to_numeric(df["value"])
    # print(df["period"])

    #  find the first period for which there is data
    first_period = pd.to_datetime(df["period"].min()).strftime("%Y")
    #  find the last period for which there is data
    end_period = pd.to_datetime(df["period"].max()).strftime("%Y")

    df_1997 = df.sort_values(by="period")

    #  save df to csv
    df_1997.to_csv(
        f"./output/natural_gas_consumption_by_end_use_{first_period}-{end_period}.csv",
        index=False,
    )

    print("Analyzing data ...")

    naturalGasConsumptionByEndUse1997(
        df_1997, facets, facet_labels, first_period, end_period
    )


if __name__ == "__main__":
    naturalGasConsumptionByEndUse()
