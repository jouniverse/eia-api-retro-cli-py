"""
Quick Fetch Runner – executes a quick-fetch definition, displays a table and
a terminal chart using plotext.
"""

import os
import pandas as pd
import plotext as plt
from tabulate import tabulate
from utils.eia_fetch import eia_fetch
from utils.quick_fetch_defs import QUICK_FETCH_DEFS

# Common group-column → label-column mappings
_LABEL_COL_MAP = {
    "seriesId": "seriesDescription",
    "seriesDescription": "seriesDescription",
    "seriesName": "seriesName",
    "msn": "seriesDescription",
    "product": "product-name",
    "product-name": "product-name",
    "process": "process-name",
    "process-name": "process-name",
    "respondent": "respondent-name",
    "type": "type-name",
    "type-name": "type-name",
    "duoarea": "duoarea-name",
    "stateId": "stateName",
    "fueltype": "fueltype",
    "fuelid": "fuelDescription",
    "fuel-name": "fuel-name",
    "countryRegionId": "countryRegionName",
    "countryRegionName": "countryRegionName",
    "productName": "productName",
    "regionName": "regionName",
    "region": "region",
    "toba": "toba",
    "sectorName": "sectorName",
}


def _resolve_group_col(df, defn):
    """Return (group_col, label_col) or (None, None)."""
    explicit = defn.get("group_col")
    if explicit and explicit in df.columns:
        label = _LABEL_COL_MAP.get(explicit, explicit)
        if label not in df.columns:
            label = explicit
        return explicit, label

    # Auto-detect
    candidates = [
        "seriesDescription",
        "seriesName",
        "product-name",
        "process-name",
        "type-name",
        "respondent-name",
        "fuel-name",
        "countryRegionName",
        "productName",
        "regionName",
        "sectorName",
        "fueltype",
        "region",
        "toba",
    ]
    for c in candidates:
        if c in df.columns and df[c].nunique() > 1:
            return c, c
    return None, None


def _primary_value_col(defn, df):
    """Return the primary value column name."""
    for col in defn["data"]:
        if col in df.columns:
            return col
    if "value" in df.columns:
        return "value"
    return defn["data"][0]


def display_table(df, defn):
    """Print a summary table of the fetched data."""
    value_col = _primary_value_col(defn, df)
    group_col, label_col = _resolve_group_col(df, defn)

    print()
    print(f"  {defn.get('label', 'Data')}")
    print(f"  Route: {defn['route']}  |  Frequency: {defn['frequency']}")

    if "period" in df.columns:
        print(f"  Period: {df['period'].min()} → {df['period'].max()}")
    print(f"  Records: {len(df)}")
    print()

    if group_col and group_col in df.columns and df[group_col].nunique() <= 30:
        rows = []
        for name, grp in df.groupby(
            label_col if label_col in df.columns else group_col
        ):
            vals = grp[value_col].dropna()
            if vals.empty:
                continue
            short_name = str(name)[:50]
            rows.append(
                {
                    "Series": short_name,
                    "Min": f"{vals.min():.2f}",
                    "Max": f"{vals.max():.2f}",
                    "Latest": f"{vals.iloc[-1]:.2f}",
                    "Records": len(vals),
                }
            )
        if rows:
            print(tabulate(rows, headers="keys", tablefmt="simple_outline"))
    elif len(defn["data"]) > 1:
        # Multiple data fields – show stats for each
        rows = []
        for col in defn["data"]:
            if col in df.columns:
                vals = pd.to_numeric(df[col], errors="coerce").dropna()
                if vals.empty:
                    continue
                rows.append(
                    {
                        "Field": col,
                        "Min": f"{vals.min():.2f}",
                        "Max": f"{vals.max():.2f}",
                        "Latest": f"{vals.iloc[-1]:.2f}",
                        "Records": len(vals),
                    }
                )
        if rows:
            print(tabulate(rows, headers="keys", tablefmt="simple_outline"))
    else:
        # Single series summary
        vals = df[value_col].dropna() if value_col in df.columns else pd.Series()
        if not vals.empty:
            print(
                f"  {value_col}: min={vals.min():.2f}  max={vals.max():.2f}  latest={vals.iloc[-1]:.2f}"
            )

    print()


def display_chart(df, defn):
    """Render a plotext time-series chart."""
    if "period" not in df.columns:
        return

    value_col = _primary_value_col(defn, df)
    if value_col not in df.columns:
        return

    group_col, label_col = _resolve_group_col(df, defn)
    freq = defn["frequency"]

    plt.clear_figure()
    plt.theme("dark")
    plt.title(defn.get("label", "Chart"))

    # Determine date format for plotext
    if freq == "hourly":
        date_fmt = plt.date_form("Y-m-dTH")
    elif freq in ("daily", "weekly"):
        date_fmt = plt.date_form("Y-m-d")
    elif freq == "monthly":
        date_fmt = plt.date_form("Y-m")
    else:
        date_fmt = plt.date_form("Y")

    has_data = False

    if group_col and group_col in df.columns and df[group_col].nunique() <= 15:
        # Multi-line chart grouped by column
        groups = df.groupby(label_col if label_col in df.columns else group_col)
        for name, grp in groups:
            grp = grp.dropna(subset=[value_col])
            if grp.empty:
                continue
            periods = grp["period"].tolist()
            values = grp[value_col].tolist()
            try:
                dates = plt.datetimes_to_string(periods)
            except Exception:
                dates = periods
            short_name = str(name)[:30]
            plt.plot(dates, values, label=short_name)
            has_data = True
    elif len(defn["data"]) > 1:
        # Multiple data columns as separate lines
        for col in defn["data"]:
            if col not in df.columns:
                continue
            clean = df.dropna(subset=[col])
            if clean.empty:
                continue
            periods = clean["period"].tolist()
            values = pd.to_numeric(clean[col], errors="coerce").tolist()
            try:
                dates = plt.datetimes_to_string(periods)
            except Exception:
                dates = periods
            plt.plot(dates, values, label=col[:30])
            has_data = True
    else:
        # Single line
        clean = df.dropna(subset=[value_col])
        if not clean.empty:
            periods = clean["period"].tolist()
            values = clean[value_col].tolist()
            try:
                dates = plt.datetimes_to_string(periods)
            except Exception:
                dates = periods
            plt.plot(dates, values, label=value_col)
            has_data = True

    if has_data:
        plt.xlabel("Period")
        plt.ylabel(value_col)
        plt.show()
        print()


def save_csv(df, key):
    """Save DataFrame to CSV in output directory."""
    output_dir = os.path.join(".", "output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{key}.csv")
    df.to_csv(path, index=False)
    print(f"  Saved: {path}")


def run_quick_fetch(key, save=False):
    """Execute a quick fetch by definition key."""
    if key not in QUICK_FETCH_DEFS:
        print(f"Unknown quick fetch key: {key}")
        return

    defn = QUICK_FETCH_DEFS[key]
    print(f"  Fetching: {defn.get('label', key)} ...")

    df = eia_fetch(
        route=defn["route"],
        frequency=defn["frequency"],
        data_fields=defn["data"],
        facets=defn.get("facets"),
        start=defn.get("start"),
        end=defn.get("end"),
        offset=defn.get("offset", 0),
        sort_dir=defn.get("sort_dir", "asc"),
        start_dynamic=defn.get("start_dynamic"),
    )

    if df is None or df.empty:
        print("  No data returned.")
        return

    display_table(df, defn)
    display_chart(df, defn)

    if save:
        save_csv(df, key)

    return df


def category_menu(title, options):
    """Generic category sub-menu. options is a list of (key, label) tuples."""
    last_key = None
    last_df = None

    while True:
        print(title.upper())
        print("-" * 100)
        for i, (_, label) in enumerate(options, 1):
            print(f"  {i}. {label}")
        print("  S. Save last fetch to CSV")
        print("  R. RETURN (-> main menu)")
        print("-" * 100)

        choice = input("Enter your choice: ").strip()

        if choice.upper() == "R":
            break
        if choice.upper() == "S":
            if last_df is not None and last_key:
                save_csv(last_df, last_key)
            else:
                print("  No data to save yet. Run a fetch first (pick a number).")
            continue

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                key = options[idx][0]
                print("-" * 100)
                result = run_quick_fetch(key)
                if result is not None:
                    last_key = key
                    last_df = result
                print("-" * 100)
            else:
                print("  Invalid choice.")
        except ValueError:
            print("  Invalid input.")
