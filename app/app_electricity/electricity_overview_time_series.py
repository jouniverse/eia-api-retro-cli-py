import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
import pandas as pd
from tabulate import tabulate
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def electricityOverviewLast7Days():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "electricity/rto/region-data/"
    url = URL_BASE + endpoint + "data"

    # Get current hour in UTC
    current_time = datetime.now(UTC)
    start_time = current_time - timedelta(days=7)
    start_hour = start_time.strftime("%Y-%m-%dT%H")
    end_time = current_time - timedelta(hours=2)
    end_hour = end_time.strftime("%Y-%m-%dT%H")

    regions = "US48"

    facets = ["D", "DF", "NG", "TI"]

    facet_labels = {
        "D": "Demand",
        "DF": "Demand Forecast",
        "NG": "Natural Gas",
        "TI": "Total Interchange",
    }

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "facets[type][]": facets,
        "facets[respondent][]": regions,
        "start": start_hour,
        "end": end_hour,
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

    # D = demand
    # DF = demand forecast
    # G = generation
    # TI = total interchange
    # print the average of facets. round to 0 decimal places
    print("-" * 100)
    print(
        f"Electricity Overview - Average of last 7 days ({start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}):"
    )
    table_data = []
    for facet in facets:
        facet_data = df[df["type"] == facet]
        facet_demand = facet_data["value"].mean()
        table_data.append([facet, facet_labels[facet], f"{facet_demand:.0f} MWh"])
    # print also average of D - DF
    avg_D = df[df["type"] == "D"]["value"].mean()
    avg_DF = df[df["type"] == "DF"]["value"].mean()
    D_DF_demand = avg_D - avg_DF
    table_data.append(["D - DF", "Demand - Demand Forecast", f"{D_DF_demand:.0f} MWh"])
    print(
        tabulate(
            table_data,
            headers=["Label", "Name", "Average Value (MWh)"],
            tablefmt="grid",
        )
    )

    # export df to csv
    df.to_csv(
        f"./output/electricity_overview_last_7_days_{current_time.strftime('%Y-%m-%d')}.csv",
        index=False,
    )

    # Ensure the period column is in datetime format
    df["period"] = pd.to_datetime(df["period"])

    plt.clear_figure()  # Clear any existing plots
    plt.date_form("d/m/Y H:M")  # Set the date format

    for facet in facets:
        facet_data = df[df["type"] == facet]
        x_values = facet_data["period"].dt.strftime("%d/%m/%Y %H:%M")
        plt.plot(x_values, facet_data["value"], label=facet)

    plt.title(
        f"Electricity Overview by Type ({start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}) - Average of last 7 days"
    )
    plt.ylabel("MWh")
    plt.theme("pro")

    plt.show()


if __name__ == "__main__":
    electricityOverviewLast7Days()
