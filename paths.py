from os import path
import json


def load_user_paths(user_paths_file):
    """Loads user-defined paths from a JSON file."""
    if path.exists(user_paths_file):
        with open(user_paths_file, "r") as f:
            return json.load(f)
    return []


def save_user_paths(paths, user_paths_file):
    """Saves user-defined paths to a JSON file."""
    with open(user_paths_file, "w") as f:
        json.dump(paths, f)
