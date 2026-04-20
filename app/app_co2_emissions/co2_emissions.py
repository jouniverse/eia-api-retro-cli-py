#  UI for CO2 emissions component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import CO2_OPTIONS


def co2_emissions():
    category_menu("CO2 EMISSIONS", CO2_OPTIONS)


if __name__ == "__main__":
    co2_emissions()
