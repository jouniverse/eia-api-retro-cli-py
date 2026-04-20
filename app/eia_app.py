from app_electricity.electricity import electricity
from app_petroleum.petroleum import petroleum
from app_total_energy.total_energy import total_energy
from app_natural_gas.natural_gas import natural_gas
from app_information.information import information
from app_crude_oil_imports.crude_oil_imports import crude_oil_imports
from app_coal.coal import coal
from app_seds.seds import seds
from app_steo.steo import steo
from app_international.international import international
from app_nuclear_outages.nuclear_outages import nuclear_outages
from app_densified_biomass.densified_biomass import densified_biomass
from app_aeo.aeo import aeo
from app_ieo.ieo import ieo
from app_co2_emissions.co2_emissions import co2_emissions

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import FEATURED_OPTIONS
from utils.download_data import download_data

#  UI for the EIA API -> selected routes
#  0. quick fetch (featured)")
#  1. electricity")
#  2. coal")
#  3. crude-oil-imports")
#  4. natural-gas")
#  5. petroleum")
#  6. seds")
#  7. steo")
#  8. total-energy")
#  9. international")
# 10. nuclear-outages")
# 11. densified-biomass")
# 12. aeo")
# 13. ieo")
# 14. co2-emissions")
# 15. information")
# 16. download data")
#  Q. QUIT")

# Print the logo
from utils.logo_art import image_to_ascii

print("-" * 100)
print("ARPANET connection established @8080")
print("-" * 100)
# Path to the image file
image_path = "./app//imgs/eia_logo.png"
# You can tweak the new_width parameter for finer or coarser results.
ascii_art = image_to_ascii(image_path, new_width=50)
print(ascii_art)


def eia_app():
    while True:
        print("*" * 100)
        print("EIA API")
        print("*" * 100)
        print("  0. quick fetch (featured)")
        print("  1. electricity")
        print("  2. coal")
        print("  3. crude-oil-imports")
        print("  4. natural-gas")
        print("  5. petroleum")
        print("  6. seds")
        print("  7. steo")
        print("  8. total-energy")
        print("  9. international")
        print(" 10. nuclear-outages")
        print(" 11. densified-biomass")
        print(" 12. aeo")
        print(" 13. ieo")
        print(" 14. co2-emissions")
        print(" 15. information")
        print(" 16. download data")
        print("  Q. QUIT")
        print("-" * 100)
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            print("-" * 100)
            category_menu("QUICK FETCH (FEATURED)", FEATURED_OPTIONS)
            print("-" * 100)
        elif choice == "1":
            print("-" * 100)
            electricity()
            print("-" * 100)
        elif choice == "2":
            print("-" * 100)
            coal()
            print("-" * 100)
        elif choice == "3":
            print("-" * 100)
            crude_oil_imports()
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
            total_energy()
            print("-" * 100)
        elif choice == "9":
            print("-" * 100)
            international()
            print("-" * 100)
        elif choice == "10":
            print("-" * 100)
            nuclear_outages()
            print("-" * 100)
        elif choice == "11":
            print("-" * 100)
            densified_biomass()
            print("-" * 100)
        elif choice == "12":
            print("-" * 100)
            aeo()
            print("-" * 100)
        elif choice == "13":
            print("-" * 100)
            ieo()
            print("-" * 100)
        elif choice == "14":
            print("-" * 100)
            co2_emissions()
            print("-" * 100)
        elif choice == "15":
            print("-" * 100)
            information()
            print("-" * 100)
        elif choice == "16":
            print("-" * 100)
            download_data()
            print("-" * 100)
        elif choice.upper() == "Q":
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
    image_path = "./app/imgs/us_map.png"
    # print US map
    ascii_art = image_to_ascii(image_path, new_width=80)
    print(ascii_art)
    print("-" * 100)
    print("ARPANET disconnected @8080")
    print("-" * 100)
