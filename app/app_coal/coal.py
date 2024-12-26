#  UI for coal component of the EIA API
#  it has ? choices:
#  1. coal consumption and quality consumption
#  2. coal consumption and quality price
#  3. return to main menu


from app_coal.coal_consumption_and_quality_consumption import (
    coalConsumptionAndQualityConsumption,
)
from app_coal.coal_consumption_and_quality_price import coalConsumptionAndQualityPrice


def coal():
    while True:
        print("COAL")
        print("-" * 100)
        print("1. coal consumption")
        print("2. coal price")
        print("R. RETURN (-> main menu)")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("-" * 100)
            print("Analyzing data ...")
            coalConsumptionAndQualityConsumption()
            print("-" * 100)
        elif choice == "2":
            print("-" * 100)
            print("Analyzing data ...")
            coalConsumptionAndQualityPrice()
            print("-" * 100)
        elif choice == "R" or choice == "r":
            print("-" * 100)
            print("Returning to main menu ...")
            print("-" * 100)
            break
        else:
            print("-" * 100)
            print("Invalid choice. Please try again.")
            print("-" * 100)


if __name__ == "__main__":
    coal()
