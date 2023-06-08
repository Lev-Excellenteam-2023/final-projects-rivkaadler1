import json


def save_list_as_json(lst: list, filename: str):
    """Save a list as JSON to a file.

    Args:
        lst (list): The list to be saved as JSON.
        filename (str): The name of the output JSON file.

    Returns:
        None
    """
    json_path = f"{filename}.json"
    with open(json_path, "w") as file:
        json.dump(lst, file)
