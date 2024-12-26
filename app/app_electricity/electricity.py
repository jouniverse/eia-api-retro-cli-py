#  UI for electricity component of the EIA API
#  it has 5 choices:
#  1. current electricity demand by region
#  2. electricity demand by region last 7 days
#  3. overview last 7 days
#  4. electricity generation by source
#  5. electricity interchange last 7 days

from app_electricity.electricity_demand_by_region_current import (
    currentElectricityDemandByRegion,
)
from app_electricity.electricity_demand_by_us48_time_series import (
    electricityDemandUS48Last7Days,
)
from app_electricity.electricity_overview_time_series import (
    electricityOverviewLast7Days,
)
from app_electricity.electricity_generation_by_source import (
    electricityGenerationBySource,
)
from app_electricity.electricity_interchange import electricityInterchangeLast7Days


def electricity():
    while True:
        print("ELECTRICITY")
        print("-" * 100)
        print("1. current electricity demand by region")
        print("2. electricity demand US48 last 7 days")
        print("3. overview last 7 days")
        print("4. electricity generation by source last 7 days")
        print("5. electricity interchange last 7 days")
        print("R. RETURN (-> main menu)")
        print("-" * 100)
        choice = input("Enter your choice: ")
        if choice == "1":
            print("-" * 100)
            print("Analyzing data ...")
            currentElectricityDemandByRegion()
            print("-" * 100)
        elif choice == "2":
            print("-" * 100)
            print("Analyzing data ...")
            electricityDemandUS48Last7Days()
            print("-" * 100)
        elif choice == "3":
            print("-" * 100)
            print("Analyzing data ...")
            electricityOverviewLast7Days()
            print("-" * 100)
        elif choice == "4":
            print("-" * 100)
            print("Analyzing data ...")
            electricityGenerationBySource()
            print("-" * 100)
        elif choice == "5":
            print("-" * 100)
            print("Analyzing data ...")
            electricityInterchangeLast7Days()
            print("-" * 100)
        elif choice == "R" or choice == "r":
            break
        else:
            print("-" * 100)
            print("Invalid choice. Please try again.")
            print("-" * 100)


if __name__ == "__main__":
    electricity()
