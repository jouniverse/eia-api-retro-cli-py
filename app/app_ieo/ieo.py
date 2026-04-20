#  UI for IEO (International Energy Outlook) component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import IEO_OPTIONS


def ieo():
    category_menu("IEO (International Energy Outlook)", IEO_OPTIONS)


if __name__ == "__main__":
    ieo()
