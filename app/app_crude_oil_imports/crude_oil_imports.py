import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def crudeOilImportsWorld(
    df,
    originIds,
    destinationIds,
    gradeIds,
    originId_labels,
    destinationId_labels,
    gradeId_labels,
):

    #  select data where the column originId = "WORLD"
    # Create an explicit copy when filtering
    df = df[df["originId"] == "WORLD"].copy()

    #  find the first period for which there is data
    first_period = pd.to_datetime(df["period"].min()).strftime("%Y")
    #  find the last period for which there is data
    end_period = pd.to_datetime(df["period"].max()).strftime("%Y")

    df["quantity"] = pd.to_numeric(df["quantity"])

    df = df.sort_values(by="period")

    #  save df to csv
    df.to_csv(
        f"./output/crude_oil_imports_world_{first_period}-{end_period}.csv",
        index=False,
    )

    table_data = []
    for idx in gradeIds:
        facet_data = df[df["gradeId"] == idx]
        min_val = facet_data["quantity"].min()
        max_val = facet_data["quantity"].max()
        range_val = max_val - min_val
        current_val = facet_data["quantity"].iloc[-1]
        table_data.append(
            [
                idx,
                gradeId_labels[idx],
                min_val,
                max_val,
                range_val,
                current_val,
            ]
        )
    print("-" * 100)
    print(f"Crude Oil Imports by Grade {first_period}-{end_period} (1000 BBL):")
    print(
        tabulate(
            table_data,
            headers=[
                "Facet",
                "Name",
                "Min",
                "Max",
                "Range",
                f"Current ({end_period})",
            ],
            tablefmt="grid",
        )
    )

    # Convert period to datetime first
    df = df[df["originId"] == "WORLD"].copy()  # Create an explicit copy
    df["period"] = pd.to_datetime(df["period"])

    plt.clear_figure()

    plt.date_form("Y")

    for idx in gradeIds:
        facet_data = df[df["gradeId"] == idx]
        x_values = facet_data["period"].dt.strftime("%Y")
        plt.plot(x_values, facet_data["quantity"], label=gradeId_labels[idx])

    plt.title(f"Crude Oil Imports by Grade {first_period}-{end_period} (1000 BBL)")
    plt.ylabel("1000 BBL")
    plt.theme("pro")

    plt.show()


def crudeOilImportsRegion(
    df,
    originIds,
    destinationIds,
    gradeIds,
    originId_labels,
    destinationId_labels,
    gradeId_labels,
):
    # Create a copy and filter for non-WORLD origins and LSW grade
    df = df[df["originId"] != "WORLD"].copy()
    df = df[df["gradeId"] == "LSW"].copy()

    #  find the first period for which there is data
    first_period = pd.to_datetime(df["period"].min()).strftime("%Y")
    #  find the last period for which there is data
    end_period = pd.to_datetime(df["period"].max()).strftime("%Y")
    # Convert quantity to numeric if not already
    df["quantity"] = pd.to_numeric(df["quantity"])

    df = df.sort_values(by="period")

    #  save df to csv
    df.to_csv(
        f"./output/crude_oil_imports_region_{first_period}-{end_period}.csv",
        index=False,
    )

    table_data = []
    for idx in originIds:
        # Skip WORLD since we filtered it out
        if idx == "WORLD":
            continue

        facet_data = df[df["originId"] == idx]

        min_val = facet_data["quantity"].min()
        max_val = facet_data["quantity"].max()
        range_val = max_val - min_val
        current_val = facet_data["quantity"].iloc[-1]

        table_data.append(
            [
                idx,
                originId_labels[idx],
                min_val,
                max_val,
                range_val,
                current_val,
            ]
        )

    print("-" * 100)
    print(
        f"Crude Oil Imports by Region {first_period}-{end_period}, LSW Grade (1000 BBL):"
    )
    print(
        tabulate(
            table_data,
            headers=[
                "Facet",
                "Name",
                "Min",
                "Max",
                "Range",
                f"Current ({end_period})",
            ],
            tablefmt="grid",
        )
    )

    # Convert period to datetime
    df["period"] = pd.to_datetime(df["period"])

    plt.clear_figure()

    plt.date_form("Y")

    # Plot each region's data
    for idx in originIds:
        # Skip WORLD since we filtered it out
        if idx == "WORLD":
            continue
        region_data = df[df["originId"] == idx]
        if len(region_data) > 0:  # Only plot if we have data
            x_values = region_data["period"].dt.strftime("%Y")
            plt.plot(x_values, region_data["quantity"], label=originId_labels[idx])

    plt.title(
        f"Crude Oil Imports by Region {first_period}-{end_period}, LSW Grade (1000 BBL)"
    )
    plt.ylabel("1000 BBL")
    plt.theme("pro")

    plt.show()


def crudeOilImports():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "crude-oil-imports/"
    # Get data
    url = URL_BASE + endpoint + "data"

    # region = U.S.
    originIds = [
        "REG_AF",
        "REG_AP",
        "REG_CA",
        "REG_EA",
        "REG_EU",
        "REG_ME",
        "REG_OA",
        "WORLD",
    ]

    originId_labels = {
        "REG_AF": "Africa",
        "REG_AP": "Asia Pacific",
        "REG_CA": "Canada",
        "REG_EA": "Eurasia",
        "REG_EU": "Europe",
        "REG_ME": "Middle East",
        "REG_OA": "Other Americas",
        "WORLD": "World",
    }

    destinationIds = ["US"]

    destinationId_labels = {
        "US": "U.S.",
    }

    gradeIds = ["HSO", "HSW", "LSO", "LSW", "MED"]

    gradeId_labels = {
        "HSO": "Heavy Sour",
        "HSW": "Heavy Sweet",
        "LSO": "Light Sour",
        "LSW": "Light Sweet",
        "MED": "Medium",
    }

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "quantity",
        "facets[originId][]": originIds,
        "facets[destinationId][]": destinationIds,
        "facets[gradeId][]": gradeIds,
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
    df["quantity"] = pd.to_numeric(df["quantity"])

    crudeOilImportsWorld(
        df,
        originIds,
        destinationIds,
        gradeIds,
        originId_labels,
        destinationId_labels,
        gradeId_labels,
    )

    crudeOilImportsRegion(
        df,
        originIds,
        destinationIds,
        gradeIds,
        originId_labels,
        destinationId_labels,
        gradeId_labels,
    )
