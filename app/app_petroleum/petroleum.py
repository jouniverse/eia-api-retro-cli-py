#  UI for petroleum component of the EIA API

from utils.quick_fetch_runner import category_menu
from utils.quick_fetch_defs import PETROLEUM_OPTIONS


def petroleum():
    category_menu("PETROLEUM", PETROLEUM_OPTIONS)


if __name__ == "__main__":
    petroleum()
