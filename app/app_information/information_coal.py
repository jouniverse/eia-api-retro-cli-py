import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import requests
from tabulate import tabulate
import pandas as pd
import plotext as plt  # type: ignore
from datetime import datetime, timedelta, UTC
from api_key import API_KEY
from app_information.print_info import printInfo

URL_BASE = "https://api.eia.gov/v2/"

#  shipments
#       mine-state-aggregates
#       receipts
#       mine-aggregates
#       plant-state-aggregates
#       plant-aggregates
#       by-mine-by-plant


def informationCoal():

    while True:
        print("COAL")
        print("-" * 100)
        print("1. shipments")
        print("R. RETURN (-> information)")

        choice = input("Enter your choice: ")
        print("-" * 100)

        if choice == "1":
            print("-" * 100)
            endpoint = "coal/shipments"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            printInfo(data)
        elif choice == "R" or choice == "r":
            print("-" * 100)
            break
        else:
            print("-" * 100)
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    informationCoal()
