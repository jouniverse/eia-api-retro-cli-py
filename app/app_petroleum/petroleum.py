#  UI for petroleum component of the EIA API
#  it has ? choices:
#  1. petroleum spot prices
#  2. weekly retail gasoline and diesel prices
#  3. current average heating oil and propane prices
#  4. crude oil production (U.S)
#  5. return to main menu

from app_petroleum.petroleum_pri_spt import petroleumSpotPrices
from app_petroleum.petroleum_pri_gnd import petroleumWeeklyRetailGasolineAndDieselPrices
from app_petroleum.petroleum_pri_wfr import petroleumWeeklyHeatingOilAndPropanePrices
from app_petroleum.petroleum_crd_crdpn import petroleumCrudeOilProduction


def petroleum():
    while True:
        print("PETROLEUM")
        print("-" * 100)
        print("1. petroleum spot prices")
        print("2. weekly retail gasoline and diesel prices")
        print("3. weekly heating oil and propane prices")
        print("4. crude oil production")
        print("R. RETURN (-> main menu)")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("-" * 100)
            print("Analyzing data ...")
            petroleumSpotPrices()
            print("-" * 100)
        elif choice == "2":
            print("-" * 100)
            print("Analyzing data ...")
            petroleumWeeklyRetailGasolineAndDieselPrices()
            print("-" * 100)
        elif choice == "3":
            print("-" * 100)
            print("Analyzing data ...")
            petroleumWeeklyHeatingOilAndPropanePrices()
            print("-" * 100)
        elif choice == "4":
            print("-" * 100)
            print("Analyzing data ...")
            petroleumCrudeOilProduction()
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
    petroleum()
