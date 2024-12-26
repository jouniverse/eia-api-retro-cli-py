import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from app.api_key import API_KEY

URL_BASE = "https://api.eia.gov/v2/"

endpoint = "steo/"

# Get data
url = URL_BASE + endpoint + "data"

# monthly: 2014-01 2025-01 ->
# "start": "2014-01",
# "end": "2025-01",
# annual: 2014 2025 ->
# "start": 2014,
# "end": 2025,
# quarterly: 2014-Q1 2025-Q1 ->
# "start": "2014-Q1",
# "end": "2025-Q1",

parameters = {
    "api_key": API_KEY,
    "offset": 0,
    "data[]": "value",
    "start": "2014-Q1",
    "end": "2025-Q1",
    "frequency": "quarterly",
    "sort[0][column]": "period",
    "sort[0][direction]": "asc",
}

data_all = []

i = 0

while True:
    res = requests.get(url, params=parameters)
    data = res.json()
    data_all.extend(data["response"]["data"])

    print(i)

    if len(data["response"]["data"]) < 5000:
        break

    parameters["offset"] += 5000

    i += 5000

df = pd.DataFrame(data_all)

# Convert value to numeric first
df["value"] = pd.to_numeric(df["value"])

#  sort df by period into ascending order
df = df.sort_values(by="period")

# from the data get all unique rows with columns "seriesId", "seriesDescription" and "unit"
df_unique = df[["seriesId", "seriesDescription", "unit"]].drop_duplicates()

#  save to csv in the form:
#  seriesId, seriesDescription, unit
# df_unique.to_csv("./steo_facets_seriesids_annual.csv", index=False)
# print("Saved to ./steo_facets_seriesids_annual.csv")
# df_unique.to_csv("./steo_facets_seriesids_monthly.csv", index=False)
# print("Saved to ./steo_facets_seriesids_monthly.csv")
df_unique.to_csv("./steo_facets_seriesids_quarterly.csv", index=False)
print("Saved to ./steo_facets_seriesids_quarterly.csv")
