#  UI for SEDS component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import SEDS_OPTIONS


def seds():
    category_menu("SEDS (State Energy Data System)", SEDS_OPTIONS)


if __name__ == "__main__":
    seds()
