#  UI for electricity component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import ELECTRICITY_OPTIONS


def electricity():
    category_menu("ELECTRICITY", ELECTRICITY_OPTIONS)


if __name__ == "__main__":
    electricity()
