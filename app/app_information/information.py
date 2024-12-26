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

from app_information.information_coal import informationCoal
from app_information.information_electricity import informationElectricity
from app_information.information_natural_gas import informationNaturalGas
from app_information.information_petroleum import informationPetroleum
from utils.api_structure import display_api_structure

# from app_information.download_data import download_data

URL_BASE = "https://api.eia.gov/v2/"

# UI for information component of the EIA API
# 1. coal
# 2. crude-oil-imports -> no routes
# 3. electricity
# 4. international -> no routes
# 5. natural-gas (id, name)
# 6. nuclear-outages
# 7. petroleum (id,name)
# 8. seds -> no routes
# 9. steo -> no routes
# 10. densified-biomass
# 11. total-energy -> no routes
# 12. aeo (id, name)
# 13. ieo (id, name)
# 14. co2-emissions


def information():
    # All available endpoints
    res = requests.get(URL_BASE, params={"api_key": API_KEY})
    data = res.json()
    # print(tabulate(data["response"]["routes"], headers="keys"))
    print("-" * 100)
    print("ALL AVAILABLE MAIN ROUTES:")
    printInfo(data)

    while True:
        # print("-" * 100)
        print("INFORMATION")
        print("-" * 100)
        print("1. coal")
        print("2. crude-oil-imports")
        print("3. electricity")
        print("4. international")
        print("5. natural-gas")
        print("6. nuclear-outages")
        print("7. petroleum")
        print("8. seds")
        print("9. steo")
        print("10. densified-biomass")
        print("11. total-energy")
        print("12. aeo")
        print("13. ieo")
        print("14. co2-emissions")
        print("15. api-structure")
        # print("16. download data")
        print("R. RETURN (-> main menu)")
        print("-" * 100)

        choice = input("Enter your choice: ")
        if choice == "1":
            print("-" * 100)
            #  coal endpoint
            endpoint = "coal"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            # print coal routes
            # print(tabulate(data["response"]["routes"], headers="keys"))
            # print("-" * 100)
            printInfo(data)
            informationCoal()
        elif choice == "2":
            print("-" * 100)
            print("No available routes for crude-oil-imports")
            print("-" * 100)
        elif choice == "3":
            print("-" * 100)
            #  electricity endpoint
            endpoint = "electricity"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            # print("-" * 100)
            printInfo(data)
            informationElectricity()
        elif choice == "4":
            print("-" * 100)
            print("No available routes for international")
            print("-" * 100)
        elif choice == "5":
            print("-" * 100)
            #  natural-gas endpoint
            endpoint = "natural-gas"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            # print("-" * 100)
            printInfo(data, reduced_cols=True)
            informationNaturalGas()
        elif choice == "6":
            print("-" * 100)
            #  nuclear-outages endpoint
            endpoint = "nuclear-outages"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            # print("-" * 100)
            printInfo(data)
        elif choice == "7":
            print("-" * 100)
            #  petroleum endpoint
            endpoint = "petroleum"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            # print("-" * 100)
            printInfo(data, reduced_cols=True)
            informationPetroleum()
        elif choice == "8":
            print("-" * 100)
            print("No available routes for seds")
            print("-" * 100)
        elif choice == "9":
            print("-" * 100)
            print("No available routes for steo")
            print("-" * 100)
        elif choice == "10":
            print("-" * 100)
            #  densified-biomass endpoint
            endpoint = "densified-biomass"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            # print("-" * 100)
            printInfo(data)
        elif choice == "11":
            print("-" * 100)
            print("No available routes for total-energy")
            print("-" * 100)
        elif choice == "12":
            print("-" * 100)
            #  aeo endpoint
            endpoint = "aeo"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            # print("-" * 100)
            printInfo(data, reduced_cols=True)
        elif choice == "13":
            print("-" * 100)
            #  ieo endpoint
            endpoint = "ieo"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            # print("-" * 100)
            printInfo(data, reduced_cols=True)
        elif choice == "14":
            print("-" * 100)
            #  co2-emissions endpoint
            endpoint = "co2-emissions"
            url = URL_BASE + endpoint
            res = requests.get(url, params={"api_key": API_KEY})
            data = res.json()
            # print("-" * 100)
            printInfo(data)
        elif choice == "15":
            print("-" * 100)
            display_api_structure()
            # print("-" * 100)
        # elif choice == "16":
        #     print("-" * 100)
        #     download_data()
        #     # print("-" * 100)
        elif choice == "R" or choice == "r":
            print("-" * 100)
            break
        else:
            print("-" * 100)
            print("Invalid choice. Please try again.")
            print("-" * 100)


if __name__ == "__main__":
    information()
