#  UI for crude oil imports component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import CRUDE_OIL_IMPORTS_OPTIONS


def crude_oil_imports():
    category_menu("CRUDE OIL IMPORTS", CRUDE_OIL_IMPORTS_OPTIONS)


if __name__ == "__main__":
    crude_oil_imports()
