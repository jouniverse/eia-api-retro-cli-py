import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
import pandas as pd
from tabulate import tabulate
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def electricityGenerationBySource():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "electricity/rto/fuel-type-data/"
    url = URL_BASE + endpoint + "data"

    # Get current hour in UTC
    current_time = datetime.now(UTC)
    # Subtract 2 hours to get the most recently completed hour's data
    query_time = current_time - timedelta(hours=2)
    query_hour = query_time.strftime("%Y-%m-%dT%H")

    regions = ["US48"]

    facets = [
        "BAT",
        "UES",
        "WAT",
        "NG",
        "SNB",
        "WND",
        "OTH",
        "COL",
        "PS",
        "SUN",
        "OIL",
        "NUC",
    ]

    facet_labels = {
        "BAT": "Battery Storage",
        "UES": "Unknown Energy Storage",
        "WAT": "Hydro",
        "NG": "Natural Gas",
        "SNB": "Solar with integrated battery storage",
        "WND": "Wind",
        "OTH": "Other",
        "COL": "Coal",
        "PS": "Pumped Storage",
        "SUN": "Solar",
        "OIL": "Petroleum",
        "NUC": "Nuclear",
    }

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[fueltype][]": facets,
        "facets[respondent][]": regions,
        "start": query_hour,
        "end": query_hour,
        "frequency": "hourly",
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

    df = df.sort_values(by="period")

    # # Fuel type data
    # Battery Storage = BAT
    # Unknown Energy Storage = UES
    # Hydro = WAT
    # Natural Gas = NG
    # Solar with integrated battery storage = SNB
    # Wind = WND
    # Other = OTH
    # Coal = COL
    # Pumped Storage = PS
    # Solar = SUN
    # Petroleum = OIL
    # Nuclear = NUC
    print("-" * 100)
    print(f"Energy Generation by Source US48 ({query_hour} UTC):")
    table_data = []
    for fueltype in df["fueltype"].unique():
        total_value = df[df["fueltype"] == fueltype]["value"].sum()
        table_data.append([fueltype, facet_labels[fueltype], f"{total_value} MWh"])
    print(tabulate(table_data, headers=["Label", "Name", "Value"], tablefmt="grid"))

    # export df to csv
    df.to_csv(
        f"./output/electricity_generation_by_source_{query_hour}.csv", index=False
    )

    plt.clear_figure()

    # Group by fuel type, sum values, and sort descending
    fueltype_sum = df.groupby("fueltype").sum().sort_values(by="value", ascending=False)

    plt.bar(fueltype_sum.index, fueltype_sum["value"])

    #  plot the average line
    average_value = fueltype_sum["value"].mean()
    plt.plot(
        [average_value] * len(fueltype_sum.index),
        label=f"Average: {average_value:.2f} MWh",
        marker="dot",
    )

    plt.theme("pro")
    plt.title(f"Energy Generation by Source US48 ({query_hour} UTC)")
    plt.ylabel("MWh")

    plt.show()


if __name__ == "__main__":
    electricityGenerationBySource()
