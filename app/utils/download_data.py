from typing import Dict, Union
from utils.api_routes import API_ROUTES, get_endpoint_path, is_endpoint
from utils.save_data import saveData, select_frequency, get_available_frequencies
from api_key import API_KEY


def print_menu_options(options: Dict[str, Union[Dict, str]], show_return: bool = True):
    """Print numbered menu options"""
    for i, key in enumerate(options.keys(), 1):
        print(f"{i}. {key}")
    if show_return:
        print("R. RETURN")
    print("-" * 100)


def handle_menu(
    options: Dict[str, Union[Dict, str]], title: str, current_path: str = ""
) -> str:
    """
    Handle menu selection and navigation.
    Returns the endpoint path if an endpoint is selected, empty string otherwise.
    """
    while True:
        print("-" * 100)
        print(f"{title.upper()}")
        print("-" * 100)
        print_menu_options(options)

        choice = input("Enter your choice: ")

        if choice.upper() == "R":
            return ""

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                selected_key = list(options.keys())[idx]
                selected_value = options[selected_key]

                new_path = f"{current_path}{selected_key}/"

                if is_endpoint(selected_value):
                    # Get available frequencies for this endpoint
                    frequencies = get_available_frequencies(new_path, API_KEY)

                    # Let user select from available frequencies
                    frequency = select_frequency(frequencies)
                    if frequency != "cancel":
                        return new_path, frequency
                    continue

                else:
                    result = handle_menu(selected_value, selected_key, new_path)
                    if result:  # If an endpoint was selected in submenu
                        return result
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'R'.")


def download_data():
    """Main download data menu function"""
    while True:
        result = handle_menu(API_ROUTES, "DOWNLOAD DATA")

        if not result:  # User selected return
            break

        endpoint, frequency = result
        print(f"Downloading data for endpoint: {endpoint}")
        print("Download can take a while...")
        try:
            saveData(endpoint, frequency)
            print(f"Data saved successfully to output/{endpoint}")
        except Exception as e:
            print(f"Error downloading data: {str(e)}")

        input("Press Enter to continue...")


if __name__ == "__main__":
    download_data()
