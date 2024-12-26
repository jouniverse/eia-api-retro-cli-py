#  UI for STEO component of the EIA API
#  1. shares of u.s. electricity generation
#  2. gdp indicators
#  3. co2 emissions


from app_steo.steo_share_of_electricity_gen import steoSharesOfUSElectricityGeneration
from app_steo.steo_gdp import steoGDPIndicators
from app_steo.steo_co2 import steoCO2Emissions


def steo():
    while True:
        print("-" * 100)
        print("STEO (Short-Term Energy Outlook)")
        print("-" * 100)
        print("1. shares of u.s. electricity generation")
        print("2. gdp indicators")
        print("3. co2 emissions")
        print("R. RETURN (-> main menu)")
        print("-" * 100)
        choice = input("Enter your choice: ")

        if choice == "1":
            print("-" * 100)
            print("Analyzing data ...")
            steoSharesOfUSElectricityGeneration()
            print("-" * 100)
        elif choice == "2":
            print("-" * 100)
            print("Analyzing data ...")
            steoGDPIndicators()
            print("-" * 100)
        elif choice == "3":
            print("-" * 100)
            print("Analyzing data ...")
            steoCO2Emissions()
            print("-" * 100)
        elif choice == "R" or choice == "r":
            print("-" * 100)
            print("Returning to main menu ...")
            break
        else:
            print("-" * 100)
            print("Invalid choice. Please try again.")
            print("-" * 100)


if __name__ == "__main__":
    steo()
