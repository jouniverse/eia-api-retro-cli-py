#  UI for international component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import INTERNATIONAL_OPTIONS


def international():
    category_menu("INTERNATIONAL", INTERNATIONAL_OPTIONS)


if __name__ == "__main__":
    international()
