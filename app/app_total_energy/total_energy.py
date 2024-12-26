#  UI for total energy
# 1. total energy annual
# 2. total energy monthly (print to file only)
# 3. R. return (-> main menu)


from app_total_energy.total_energy_annual import totalEnergyAnnual
from app_total_energy.total_energy_monthly import totalEnergyMonthly


def total_energy():
    while True:
        print("-" * 100)
        print("Total Energy")
        print("-" * 100)
        print("1. total energy annual")
        print("2. total energy monthly (save to file only)")
        print("R. return (-> main menu)")
        print("-" * 100)
        choice = input("Enter your choice: ")

        if choice == "1":
            print("-" * 100)
            print("Analyzing data ...")
            totalEnergyAnnual()
            print("-" * 100)
        elif choice == "2":
            print("-" * 100)
            print("Analyzing data ...")
            totalEnergyMonthly()
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
    total_energy()
