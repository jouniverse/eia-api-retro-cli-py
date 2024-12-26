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

# natural-gas
#       sum
#       pri
#       enr
#       prod
#       move
#       stor
#       cons


def informationNaturalGas():

    while True:
        print("NATURAL GAS")
        print("-" * 100)
        print("1. sum")
        print("2. pri")
        print("3. enr")
        print("4. prod")
        print("5. move")
        print("6. stor")
        print("7. cons")
        print("R. RETURN (-> information)")

        choice = input("Enter your choice: ")
        print("-" * 100)

        if choice == "1":
            endpoint = "natural-gas/sum"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            printInfo(data)
        elif choice == "2":
            endpoint = "natural-gas/pri"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            printInfo(data)
        elif choice == "3":
            endpoint = "natural-gas/enr"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            printInfo(data)
        elif choice == "4":
            endpoint = "natural-gas/prod"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            printInfo(data)
        elif choice == "5":
            endpoint = "natural-gas/move"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            printInfo(data)
        elif choice == "6":
            endpoint = "natural-gas/stor"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            printInfo(data)
        elif choice == "7":
            endpoint = "natural-gas/cons"
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
    informationNaturalGas()
