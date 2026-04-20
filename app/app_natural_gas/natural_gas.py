#  UI for natural gas component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import NATURAL_GAS_OPTIONS


def natural_gas():
    category_menu("NATURAL GAS", NATURAL_GAS_OPTIONS)


if __name__ == "__main__":
    natural_gas()
