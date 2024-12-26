import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
import pandas as pd
from tabulate import tabulate
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def currentElectricityDemandByRegion():
    URL_BASE = "https://api.eia.gov/v2/"
    endpoint = "electricity/rto/region-data/"
    url = URL_BASE + endpoint + "data"

    # Get current hour in UTC
    current_time = datetime.now(UTC)
    # Subtract 2 hours to get the most recently completed hour's data
    query_time = current_time - timedelta(hours=2)
    query_hour = query_time.strftime("%Y-%m-%dT%H")

    regions = [
        "CAL",
        "CAR",
        "CENT",
        "FLA",
        "MIDA",
        "MIDW",
        "NE",
        "NW",
        "NY",
        "SE",
        "SW",
        "TEN",
        "TEX",
        "US48",
    ]

    # Region/Country Code,Region/Country Name,Time Zone
    # CAL,California,Pacific
    # CAR,Carolinas,Eastern
    # CENT,Central,Central
    # FLA,Florida,Eastern
    # MIDA,Mid-Atlantic,Eastern
    # MIDW,Midwest,Eastern
    # NE,New England,Eastern
    # NW,Northwest,Mountain
    # NY,New York,Eastern
    # SE,Southeast,Central
    # SW,Southwest,Arizona
    # TEN,Tennessee,Central
    # TEX,Texas,Central
    # US48,United States Lower 48,Eastern

    region_labels = {
        "CAL": "California",
        "CAR": "Carolinas",
        "CENT": "Central",
        "FLA": "Florida",
        "MIDA": "Mid-Atlantic",
        "MIDW": "Midwest",
        "NE": "New England",
        "NW": "Northwest",
        "NY": "New York",
        "SE": "Southeast",
        "SW": "Southwest",
        "TEN": "Tennessee",
        "TEX": "Texas",
        "US48": "United States Lower 48",
    }

    facets = "D"

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[type][]": facets,
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

    # sort the dataframe by value in descending order
    df = df.sort_values(by="value", ascending=False)

    print("-" * 100)
    print(f"Electricity Demand by Region ({query_hour} UTC):")
    # Print demand by region in a table
    table_data = []
    for region in regions:
        region_data = df[df["respondent"] == region]
        if not region_data.empty:
            region_name = region_labels.get(region, "Unknown")
            table_data.append(
                [region, region_name, f"{region_data['value'].values[0]:,.0f}"]
            )
    print(
        tabulate(
            table_data, headers=["Region", "Name", "Demand (MWh)"], tablefmt="grid"
        )
    )

    # export df to csv
    df.to_csv(
        f"./output/electricity_demand_by_region_current_{query_hour}.csv", index=False
    )

    # plot respondent (x) vs value (y), exclude US48
    us48_data = df[df["respondent"] == "US48"]
    if not us48_data.empty:
        us48_value = us48_data["value"].values[0]
    else:
        us48_value = None

    df = df[df["respondent"] != "US48"]
    df["value"] = pd.to_numeric(df["value"])

    plt.clear_figure()  # Clear any existing plots

    plt.bar(df["respondent"], df["value"])
    plt.title(f"Electricity Demand by Region ({query_hour} UTC)")
    plt.theme("pro")

    average_value = df["value"].mean()
    plt.plot(
        [average_value] * len(df["respondent"]),
        label=f"Average: {average_value:.2f} MWh",
        marker="dot",
    )

    plt.ylabel("MWh")
    plt.show()


if __name__ == "__main__":
    currentElectricityDemandByRegion()
