#  UI for SEDS component of the EIA API
#  Only solar data is shown
#  it has 2 choices:
#  1. solar generation 1960-
#  2. solar consumption 1960-
#  3. return to main menu


from app_seds.seds_solar_gen import sedsSolarGeneration
from app_seds.seds_solar_cons import sedsSolarConsumption


def seds():
    while True:
        print("-" * 100)
        print("SEDS (State Energy Data System)")
        print("-" * 100)
        print("1. solar generation trend")
        print("2. solar consumption trend")
        print("R. RETURN (-> main menu)")
        print("-" * 100)

        choice = input("Enter your choice: ")
        if choice == "1":
            print("-" * 100)
            print("Analyzing data ...")
            sedsSolarGeneration()
            print("-" * 100)
        elif choice == "2":
            print("-" * 100)
            print("Analyzing data ...")
            sedsSolarConsumption()
            print("-" * 100)
        elif choice == "R" or choice == "r":
            print("-" * 100)
            print("Returning to main menu ...")
            # print("-" * 100)
            break
        else:
            print("-" * 100)
            print("Invalid choice. Please try again.")
            print("-" * 100)


if __name__ == "__main__":
    seds()
