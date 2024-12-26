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

# petroleum
#       sum
#       pri
#       crd
#       pnp
#       move
#       stoc
#       cons


def informationPetroleum():

    while True:
        print("PETROLEUM")
        print("-" * 100)
        print("1. sum")
        print("2. pri")
        print("3. crd")
        print("4. pnp")
        print("5. move")
        print("6. stoc")
        print("7. cons")
        print("R. RETURN (-> information)")

        choice = input("Enter your choice: ")
        print("-" * 100)

        if choice == "1":
            endpoint = "petroleum/sum"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            printInfo(data)
        elif choice == "2":
            endpoint = "petroleum/pri"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            printInfo(data)
        elif choice == "3":
            endpoint = "petroleum/crd"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            printInfo(data)
        elif choice == "4":
            endpoint = "petroleum/pnp"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            printInfo(data)
        elif choice == "5":
            endpoint = "petroleum/move"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            printInfo(data)
        elif choice == "6":
            endpoint = "petroleum/stoc"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            printInfo(data)
        elif choice == "7":
            endpoint = "petroleum/cons"
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
            print("-" * 100)


if __name__ == "__main__":
    informationPetroleum()
