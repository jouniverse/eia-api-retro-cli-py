import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def naturalGasImportVolumes():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "natural-gas/move/impc/"

    # Get available time range
    url_time = URL_BASE + endpoint
    res_time = requests.get(url_time, params={"api_key": API_KEY})
    data_time = res_time.json()

    # Start time = first year %Y, end year = last year %Y
    start_time = datetime.strptime(data_time["response"]["startPeriod"], "%Y-%m")
    start_year = start_time.strftime("%Y")
    end_time = datetime.strptime(data_time["response"]["endPeriod"], "%Y-%m")
    end_year = end_time.strftime("%Y")

    # Get data
    url = URL_BASE + endpoint + "data"

    # region = U.S.
    regions = ["NUS-Z00"]

    region_labels = {
        "NUS-Z00": "U.S.",
    }

    facets = ["IML", "INC", "IRP"]

    facet_labels = {
        "IML": "Liquefied Natural Gas Imports",
        "INC": "Compressed Natural Gas Imports",
        "IRP": "Pipeline Imports",
    }

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[duoarea][]": regions,
        "facets[process][]": facets,
        "start": start_year,
        "end": end_year,
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

    #  find the first period for which there is data
    first_period = pd.to_datetime(df["period"].min()).strftime("%Y")

    # Order df by column period into ascending order    before plotting
    df = df.sort_values(by="period")

    #  save df to csv
    df.to_csv(
        f"./output/natural_gas_imports_by_import_type_{first_period}-{end_year}.csv",
        index=False,
    )

    table_data = []
    for facet in facets:
        facet_data = df[df["process"] == facet]
        min_val = facet_data["value"].min()
        max_val = facet_data["value"].max()
        range_val = max_val - min_val
        mean_val = facet_data["value"].mean()
        table_data.append(
            [facet, facet_labels[facet], min_val, max_val, range_val, mean_val]
        )
    print("-" * 100)
    print(f"Natural Gas Imports by Import Type {first_period}-{end_year} (MMCF):")
    print(
        tabulate(
            table_data,
            headers=["Facet", "Name", "Min", "Max", "Range", "Mean"],
            tablefmt="grid",
        )
    )

    # Convert period to datetime first
    df["period"] = pd.to_datetime(df["period"])

    plt.clear_figure()
    # plt.plotsize(300, 50)
    plt.date_form("Y")

    for facet in facets:
        facet_data = df[df["process"] == facet]
        x_values = facet_data["period"].dt.strftime("%Y")
        plt.plot(x_values, facet_data["value"], label=facet)

    plt.title(f"Natural Gas Imports by Import Type {first_period}-{end_year} (MMCF)")
    plt.ylabel("MMCF")
    plt.theme("pro")
    plt.show()
