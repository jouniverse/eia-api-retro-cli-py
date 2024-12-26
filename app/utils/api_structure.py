from typing import Dict, Union
import os


def print_api_structure(
    structure: Dict[str, Union[Dict, str]], indent: str = "", is_last: bool = True
) -> None:
    """
    Prints the EIA API structure as a directory tree in the terminal.

    Args:
        structure (Dict): The API structure to print
        indent (str): Current indentation level
        is_last (bool): Whether the current item is the last in its level
    """
    for i, (key, value) in enumerate(structure.items()):
        is_current_last = i == len(structure) - 1

        # Create branch symbols
        branch = "└── " if is_current_last else "├── "

        # Print current node
        print(f"{indent}{branch}{key}")

        # Prepare indentation for children
        child_indent = indent + ("    " if is_current_last else "│   ")

        # Recursively print children if they exist
        if isinstance(value, dict):
            print_api_structure(value, child_indent, is_current_last)


def parse_api_structure(file_path: str) -> Dict:
    """
    Parses the API structure file and returns a dictionary representation.

    Args:
        file_path (str): Path to the API structure file

    Returns:
        Dict: Nested dictionary representing the API structure
    """
    structure = {}
    current_path = []
    current_indent = 0

    with open(file_path, "r") as f:
        for line in f:
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith("#"):
                continue

            # Calculate indent level
            indent = len(line) - len(line.lstrip())
            name = line.strip()

            # Adjust current path based on indent
            if indent > current_indent:
                current_path.append(prev_name)
            elif indent < current_indent:
                levels_up = (current_indent - indent) // 4
                current_path = current_path[:-levels_up]

            # Update current position
            current_indent = indent
            prev_name = name

            # Add to structure
            current_dict = structure
            for path_part in current_path:
                if path_part not in current_dict:
                    current_dict[path_part] = {}
                current_dict = current_dict[path_part]
            current_dict[name] = {}

    return structure


def display_api_structure(file_path: str = "./utils/api-structure.txt") -> None:
    """
    Main function to display the EIA API structure.

    Args:
        file_path (str): Path to the API structure file
    """
    try:
        structure = parse_api_structure(file_path)
        print("\nEIA API Structure:")
        print("─" * 50)
        print_api_structure(structure)
        print("─" * 50)
    except FileNotFoundError:
        print(f"Error: Could not find the API structure file at {file_path}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    display_api_structure()
