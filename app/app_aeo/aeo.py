#  UI for AEO (Annual Energy Outlook) component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import AEO_OPTIONS


def aeo():
    category_menu("AEO (Annual Energy Outlook)", AEO_OPTIONS)


if __name__ == "__main__":
    aeo()
