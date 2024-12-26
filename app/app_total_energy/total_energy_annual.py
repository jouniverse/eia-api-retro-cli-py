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


def totalEnergyAnnual():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "total-energy/"

    # Get available time range
    end_year = datetime.now().strftime("%Y")

    # Get data
    url = URL_BASE + endpoint + "data"

    parameters = {
        "api_key": API_KEY,
        "offset": 0,
        "data[]": "value",
        "start": end_year,
        "end": end_year,
        "frequency": "annual",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
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

    #  sort df by period into ascending order
    df = df.sort_values(by="period")

    # drop columns "period" and "msn"
    df = df.drop(columns=["period", "msn"])

    #  save df to csv
    df.to_csv(
        f"./output/total_energy_{end_year}.csv",
        index=False,
    )

    #  tabulate the columns seriesDescription, value and unit in df
    # Create a vertical-style table for better readability
    lines = []
    separator = "-" * 40  # Separator line between records

    for _, row in df.iterrows():
        lines.append(separator)
        lines.append(f"{row['seriesDescription']}")
        lines.append(f"Value: {row['value']}")
        lines.append(f"Unit: {row['unit']}")
    lines.append(separator)  # Add a final separator

    # Join the lines into a single string for output
    table = "\n".join(lines)

    # Print the table
    print(f"Energy Data Summary {end_year}")
    print(table)
    print("Returning to main menu ...")
    print("- -" * 20)
