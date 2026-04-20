#  UI for densified biomass component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import DENSIFIED_BIOMASS_OPTIONS


def densified_biomass():
    category_menu("DENSIFIED BIOMASS", DENSIFIED_BIOMASS_OPTIONS)


if __name__ == "__main__":
    densified_biomass()
