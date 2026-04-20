#  UI for nuclear outages component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import NUCLEAR_OUTAGES_OPTIONS


def nuclear_outages():
    category_menu("NUCLEAR OUTAGES", NUCLEAR_OUTAGES_OPTIONS)


if __name__ == "__main__":
    nuclear_outages()
