from app_electricity.electricity import electricity
from app_petroleum.petroleum import petroleum
from app_total_energy.total_energy import total_energy
from app_natural_gas.natural_gas import natural_gas
from app_information.information import information
from app_crude_oil_imports.crude_oil_imports import crudeOilImports
from app_coal.coal import coal
from app_seds.seds import seds
from app_steo.steo import steo

from utils.download_data import download_data

#  UI for the EIA API -> selected routes
#  1. electricity
#  2. coal
#  3. crude-oil-imports
#  4. natural-gas
#  5. petroleum
#  6. seds
#  7. steo
#  8. total-energy
#  9. information
#  10. download data
#  Q. quit

# Print the logo
from utils.logo_art import image_to_ascii

# Path to the image file
image_path = "./imgs/eia_logo.png"
# You can tweak the new_width parameter for finer or coarser results.
ascii_art = image_to_ascii(image_path, new_width=50)
print(ascii_art)


def eia_app():
    while True:
        print("*" * 100)
        print("EIA API")
        print("*" * 100)
        print("1. electricity")
        print("2. coal")
        print("3. crude-oil-imports")
        print("4. natural-gas")
        print("5. petroleum")
        print("6. seds")
        print("7. steo")
        print("8. total-energy")
        print("9. information")
        print("10. download data")
        print("Q. QUIT")
        print("-" * 100)
        choice = input("Enter your choice: ")
        if choice == "1":
            print("-" * 100)
            electricity()
            print("-" * 100)
        elif choice == "2":
            print("-" * 100)
            print("-" * 100)
            coal()
            print("-" * 100)
        elif choice == "3":
            print("-" * 100)
            crudeOilImports()
            print("-" * 100)
        elif choice == "4":
            print("-" * 100)
            natural_gas()
            print("-" * 100)
        elif choice == "5":
            print("-" * 100)
            petroleum()
            print("-" * 100)
        elif choice == "6":
            print("-" * 100)
            seds()
            print("-" * 100)
        elif choice == "7":
            print("-" * 100)
            steo()
            print("-" * 100)
        elif choice == "8":
            print("-" * 100)
            print("Analyzing data ...")
            total_energy()
            print("-" * 100)
        elif choice == "9":
            print("-" * 100)
            print("Analyzing data ...")
            information()
            print("-" * 100)
        elif choice == "10":
            print("-" * 100)
            print("Analyzing data ...")
            download_data()
            print("-" * 100)
        elif choice == "Q" or choice == "q":
            break
        else:
            print("-" * 100)
            print("Invalid choice. Please try again.")
            print("-" * 100)


if __name__ == "__main__":
    eia_app()

    print("*" * 100)
    print("Thank you for using the EIA API!")
    print("*" * 100)
    # Path to the image file
    image_path = "./imgs/us_map.png"
    # print US map
    ascii_art = image_to_ascii(image_path, new_width=80)
    print(ascii_art)
    print("-" * 100)
