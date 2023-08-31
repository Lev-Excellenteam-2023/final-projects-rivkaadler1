import json


def save_list_as_json(lst: list, path: str):
    """Save a list as JSON to a file.

    Args:
        lst (list): The list to be saved as JSON.
        path (str): The path to the output JSON file.

    Returns:
        None
    """
    json_path = f"{path}.json"
    with open(json_path, "w") as file:
        json.dump(lst, file)