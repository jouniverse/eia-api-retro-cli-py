import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY


def get_available_frequencies(endpoint: str, api_key: str) -> list:
    """Get available frequencies for the endpoint"""
    URL_BASE = "https://api.eia.gov/v2/"

    try:
        # Get metadata about the endpoint
        res = requests.get(URL_BASE + endpoint, params={"api_key": api_key})
        res.raise_for_status()
        data = res.json()

        # Check if frequency information exists in response
        if "frequency" in data["response"]:
            # Extract just the frequency IDs and their descriptions
            return [
                (freq["id"], freq["description"])
                for freq in data["response"]["frequency"]
            ]

    except Exception as e:
        print(f"Error getting frequencies: {str(e)}")

    return []


def select_frequency(available_frequencies: list = None) -> str:
    """
    Menu for frequency selection

    Args:
        available_frequencies (list): List of tuples (frequency_id, description)
    """
    while True:
        print("-" * 100)
        print("FREQUENCY")
        print("-" * 100)

        # Show only available frequencies if provided
        if available_frequencies:
            for i, (freq_id, desc) in enumerate(available_frequencies, 1):
                print(f"{i}. {freq_id} - {desc}")
        else:
            print("No frequency information available")

        print("D. default")
        print("C. CANCEL")
        print("-" * 100)

        choice = input("Enter your choice: ").upper()

        if choice == "D":
            return "default"
        elif choice == "C":
            return "cancel"

        try:
            idx = int(choice) - 1
            if available_frequencies and 0 <= idx < len(available_frequencies):
                return available_frequencies[idx][0]  # Return just the frequency ID
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number, 'D', or 'C'")


def saveData(endpoint: str, frequency: str = "default"):
    """
    Save data from the EIA API

    Args:
        endpoint (str): API endpoint
        frequency (str): Data frequency (default, quarterly, annual, etc.)
    """
    if frequency == "cancel":
        return

    URL_BASE = "https://api.eia.gov/v2/"
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, "output", endpoint.strip("/"))

    # Try direct data endpoint first
    url = URL_BASE + endpoint + "data"
    parameters = {"api_key": API_KEY, "offset": 0}

    # Add frequency parameter if specified
    if frequency != "default":
        parameters["frequency"] = frequency

    try:
        # First try to get data directly
        # print("Trying direct data download...")
        res = requests.get(url, params=parameters)
        res.raise_for_status()
        data = res.json()

        data_all = []
        endpoints = []

        # Check if we got valid data response
        if "data" in data["response"]:
            # Get the actual data
            while True:
                # print(f"Fetching data with offset {parameters['offset']}...")
                if isinstance(data["response"]["data"], list):
                    data_all.extend(data["response"]["data"])
                    # print(f"Retrieved {len(data['response']['data'])} records")
                else:
                    print("Unexpected data format in response")
                    print(data["response"]["data"])
                    break

                if len(data["response"]["data"]) < 5000:
                    break

                parameters["offset"] = parameters.get("offset", 0) + 5000
                res = requests.get(url, params=parameters)
                res.raise_for_status()
                data = res.json()

        if not data_all:
            # print("No data retrieved directly. Checking for data series...")
            # If direct data fetch failed, try getting data series first
            endpoints_url = URL_BASE + endpoint
            res = requests.get(endpoints_url, params={"api_key": API_KEY})
            res.raise_for_status()
            data = res.json()

            if "data" in data["response"]:
                try:
                    if isinstance(data["response"]["data"], list):
                        for item in data["response"]["data"]:
                            if isinstance(item, dict) and "id" in item:
                                endpoints.append(item["id"])
                            elif isinstance(item, str):
                                endpoints.append(item)
                except Exception as e:
                    print(f"Error extracting data IDs: {str(e)}")
                    print("Response data structure:", data["response"]["data"])
                    return

            if endpoints:
                print(f"Found {len(endpoints)} data series")
                parameters = {
                    "api_key": API_KEY,
                    "offset": 0,
                    "data[]": endpoints,
                    "sort[0][column]": "period",
                    "sort[0][direction]": "asc",
                }

                while True:
                    print(f"Fetching data with offset {parameters['offset']}...")
                    res = requests.get(url, params=parameters)
                    res.raise_for_status()
                    data = res.json()

                    if "data" in data["response"]:
                        if isinstance(data["response"]["data"], list):
                            data_all.extend(data["response"]["data"])
                            print(f"Retrieved {len(data['response']['data'])} records")
                        else:
                            print("Unexpected data format in response")
                            print(data["response"]["data"])
                            break

                    if len(data["response"]["data"]) < 5000:
                        break

                    parameters["offset"] = parameters.get("offset", 0) + 5000

        if not data_all:
            print("No data retrieved")
            return

        print(f"Total records retrieved: {len(data_all)}")

        # Create DataFrame
        df = pd.DataFrame(data_all)
        # print("DataFrame columns:", df.columns.tolist())

        # Convert values to numeric if possible
        if endpoints:
            for endpointId in endpoints:
                if endpointId in df.columns:
                    df[endpointId] = pd.to_numeric(df[endpointId], errors="coerce")

        # Order df by column period into ascending order
        if "period" in df.columns and not df["period"].is_monotonic_increasing:
            df = df.sort_values(by="period")

        first_period = (
            pd.to_datetime(df["period"].min()).strftime("%Y")
            if "period" in df.columns
            else "0000"
        )
        end_period = (
            pd.to_datetime(df["period"].max()).strftime("%Y")
            if "period" in df.columns
            else "9999"
        )

        # Create output folder if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # print(f"Saving data to: {output_dir}")

        # Save to CSV
        csv_path = os.path.join(
            output_dir, f"data_{frequency}_{first_period}_{end_period}.csv"
        )
        df.to_csv(csv_path, index=False)
        # print(f"Saved CSV file: {csv_path}")

        # Save to JSON
        json_path = os.path.join(
            output_dir, f"data_{frequency}_{first_period}_{end_period}.json"
        )
        with open(json_path, "w") as f:
            json.dump(data_all, f)
        # print(f"Saved JSON file: {json_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {str(e)}")
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        import traceback

        traceback.print_exc()
