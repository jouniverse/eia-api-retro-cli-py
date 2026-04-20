import requests
import pandas as pd
from datetime import datetime, timedelta
from api_key import API_KEY

URL_BASE = "https://api.eia.gov/v2/"


def compute_dynamic_start(cfg):
    """Compute start date string from dynamic config.

    cfg keys:
      unit   – "years", "months", or "days"
      amount – int
      annual / monthly / hourly – bool (date format flag)
    """
    now = datetime.utcnow()

    unit = cfg.get("unit", "years")
    amount = cfg.get("amount", 0)

    if unit == "years":
        d = now.replace(year=now.year - amount)
    elif unit == "months":
        month = now.month - amount
        year = now.year
        while month < 1:
            month += 12
            year -= 1
        d = now.replace(year=year, month=month)
    elif unit == "days":
        d = now - timedelta(days=amount)
    else:
        d = now

    if cfg.get("annual"):
        return str(d.year)
    if cfg.get("monthly"):
        return d.strftime("%Y-%m")
    if cfg.get("hourly"):
        return d.strftime("%Y-%m-%dT%H")
    return d.strftime("%Y-%m-%d")


def eia_fetch(
    route,
    frequency,
    data_fields,
    facets=None,
    start=None,
    end=None,
    offset=0,
    sort_col="period",
    sort_dir="asc",
    start_dynamic=None,
):
    """Fetch data from EIA API v2 with paging. Returns DataFrame or None."""
    if not API_KEY:
        print("Error: API key is not set. Please set your key in app/api_key.py")
        return None

    if route.endswith("/"):
        route = route[:-1]
    url = f"{URL_BASE}{route}/data"

    # Resolve dynamic start
    if start_dynamic and not start:
        start = compute_dynamic_start(start_dynamic)

    params = {
        "api_key": API_KEY,
        "offset": offset,
        "frequency": frequency,
        "sort[0][column]": sort_col,
        "sort[0][direction]": sort_dir,
        "length": 5000,
    }

    for i, field in enumerate(data_fields):
        params[f"data[{i}]"] = field

    if facets:
        for key, values in facets.items():
            if isinstance(values, list):
                for v in values:
                    params.setdefault(f"facets[{key}][]", [])
                    if isinstance(params[f"facets[{key}][]"], list):
                        params[f"facets[{key}][]"].append(v)
                    else:
                        params[f"facets[{key}][]"] = [params[f"facets[{key}][]"], v]
            else:
                params[f"facets[{key}][]"] = values

    if start:
        params["start"] = start
    if end:
        params["end"] = end

    data_all = []
    page = 0
    while True:
        try:
            res = requests.get(url, params=params)
            data = res.json()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

        if "response" not in data:
            error_msg = data.get("error", "Unknown error")
            print(f"API Error: {error_msg}")
            return None

        if "data" not in data["response"] or not data["response"]["data"]:
            if page == 0:
                print("No data available for this query.")
            break

        rows = data["response"]["data"]
        data_all.extend(rows)

        if len(rows) < 5000:
            break

        page += 1
        params["offset"] = offset + (page * 5000)

    if not data_all:
        return None

    df = pd.DataFrame(data_all)

    # Convert value columns to numeric
    for col in data_fields:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "value" in df.columns and "value" not in data_fields:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Sort by period
    if "period" in df.columns:
        df = df.sort_values(by="period").reset_index(drop=True)

    return df
