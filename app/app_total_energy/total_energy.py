#  UI for total energy component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import TOTAL_ENERGY_OPTIONS


def total_energy():
    category_menu("TOTAL ENERGY", TOTAL_ENERGY_OPTIONS)


if __name__ == "__main__":
    total_energy()
