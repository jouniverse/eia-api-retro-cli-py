import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def steoGDPIndicatorsOECD(df, end_period):
    plt.clear_figure()

    plt.date_form("Y")

    seriesId_pct = [
        "RGDPQ_OECD_PCT",
    ]

    seriesId_val = [
        "RGDPQ_OECD",
    ]

    # Plotting for seriesId_pct on the left y-axis
    for idx in seriesId_pct:
        facet_data = df[df["seriesId"] == idx]
        if len(facet_data) > 0:  # Only plot if we have data
            x_values = facet_data["period"].dt.strftime("%Y")
            plt.plot(
                x_values,
                facet_data["value"],
                label=idx,
                xside="lower",
                yside="left",
            )

    # Plotting for seriesId_val on the right y-axis
    for idx in seriesId_val:
        facet_data = df[df["seriesId"] == idx]
        if len(facet_data) > 0:  # Only plot if we have data
            x_values = facet_data["period"].dt.strftime("%Y")
            plt.plot(
                x_values,
                facet_data["value"],
                label=idx,
                xside="upper",
                yside="right",
            )

    plt.title(f"GDP Indicators OECD (-{end_period})")
    plt.ylabel("GDP (%)")
    plt.theme("pro")

    plt.show()


def steoGDPIndicators():
    URL_BASE = "https://api.eia.gov/v2/"

    endpoint = "steo/"

    # Get data
    url = URL_BASE + endpoint + "data"

    # region = U.S.
    seriesIds = [
        "GDPQXUS",
        "GDPQXUS_PCT",
        "RGDPQ_OECD",
        "RGDPQ_OECD_PCT",
        "TETC_EXP_SHR",
    ]

    series_labels = {
        "GDPQXUS": "Real GDP",
        "GDPQXUS_PCT": "Real GDP, % Change From Prior Year",
        "RGDPQ_OECD": "OECD Real GDP",
        "RGDPQ_OECD_PCT": "OECD Real GDP, % Change From Prior Year",
        "TETC_EXP_SHR": "Total U.S. Real Energy Expenditures / U.S. Real GDP",
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
    df.to_csv(f"./output/gdp_indicators_{first_period}-{end_period}.csv", index=False)

    #  Convert facets[seriesId][] = "TETC_EXP_SHR" from fraction to %
    df.loc[df["seriesId"] == "TETC_EXP_SHR", "value"] = (
        df.loc[df["seriesId"] == "TETC_EXP_SHR", "value"] * 100
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
        print(f"GDP Indicators {first_period}-{end_period}")
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

    seriesId_pct = [
        "GDPQXUS_PCT",
        "TETC_EXP_SHR",
    ]

    seriesId_val = ["GDPQXUS"]

    # Plotting for seriesId_pct on the left y-axis
    for idx in seriesId_pct:
        facet_data = df[df["seriesId"] == idx]
        if len(facet_data) > 0:  # Only plot if we have data
            x_values = facet_data["period"].dt.strftime("%Y")
            plt.plot(
                x_values,
                facet_data["value"],
                label=idx,
                xside="lower",
                yside="left",
            )

    # Plotting for seriesId_val on the right y-axis
    for idx in seriesId_val:
        facet_data = df[df["seriesId"] == idx]
        if len(facet_data) > 0:  # Only plot if we have data
            x_values = facet_data["period"].dt.strftime("%Y")
            plt.plot(
                x_values,
                facet_data["value"],
                label=idx,
                xside="upper",
                yside="right",
            )

    plt.title(f"GDP Indicators {first_period}-{end_period}")
    plt.ylabel("GDP (%)")
    plt.theme("pro")

    plt.show()

    steoGDPIndicatorsOECD(df, end_period)


if __name__ == "__main__":
    steoGDPIndicators()
