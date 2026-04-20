#  UI for coal component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import COAL_OPTIONS


def coal():
    category_menu("COAL", COAL_OPTIONS)


if __name__ == "__main__":
    coal()
