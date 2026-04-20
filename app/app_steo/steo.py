#  UI for STEO component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import STEO_OPTIONS


def steo():
    category_menu("STEO (Short-Term Energy Outlook)", STEO_OPTIONS)


if __name__ == "__main__":
    steo()
