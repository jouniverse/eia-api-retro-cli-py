#  UI for natural gas component of the EIA API
#  it has 5 choices:
#  1. natural gas price summary
#  2. natural gas gas price futures and spot prices
#  3. natural gas import prices
#  4. natural gas export prices
#  5. natural gas consumption by end use
#  6. natural gas price trends 1973-
#  7. return to main menu

from app_natural_gas.natural_gas_pri_sum import naturalGasPriceSummary
from app_natural_gas.natural_gas_pri_sum_tseries import naturalGasPriceTrends
from app_natural_gas.natural_gas_pri_fut import naturalGasGasPriceFuturesAndSpotPrices
from app_natural_gas.natural_gas_move_impc import naturalGasImportVolumes
from app_natural_gas.natural_gas_move_expc import naturalGasExportVolumes
from app_natural_gas.natural_gas_cons_sum import naturalGasConsumptionByEndUse


def natural_gas():
    while True:
        print("NATURAL GAS")
        print("-" * 100)
        print("1. natural gas price summary")
        print("2. natural gas price futures and spot prices")
        print("3. natural gas import volumes")
        print("4. natural gas export volumes")
        print("5. natural gas consumption by end use 1930-")
        print("6. natural gas price trends 1973-")
        print("R. RETURN (-> main menu)")
        print("-" * 100)
        choice = input("Enter your choice: ")
        if choice == "1":
            print("-" * 100)
            print("Analyzing data ...")
            naturalGasPriceSummary()
            print("-" * 100)
        elif choice == "2":
            print("-" * 100)
            print("Analyzing data ...")
            naturalGasGasPriceFuturesAndSpotPrices()
            print("-" * 100)
        elif choice == "3":
            print("-" * 100)
            print("Analyzing data ...")
            naturalGasImportVolumes()
            print("-" * 100)
        elif choice == "4":
            print("-" * 100)
            print("Analyzing data ...")
            naturalGasExportVolumes()
            print("-" * 100)
        elif choice == "5":
            print("-" * 100)
            print("Analyzing data ...")
            naturalGasConsumptionByEndUse()
            print("-" * 100)
        elif choice == "6":
            print("-" * 100)
            print("Analyzing data ...")
            naturalGasPriceTrends()
            print("-" * 100)
        elif choice == "R" or choice == "r":
            break
        else:
            print("-" * 100)
            print("Invalid choice. Please try again.")
            print("-" * 100)


if __name__ == "__main__":
    natural_gas()
