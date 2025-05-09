from os import path
import json
import os


def load_user_paths(user_paths_file):
    """Loads user-defined paths from a JSON file."""
    if path.exists(user_paths_file):
        with open(user_paths_file, "r") as f:
            return json.load(f)
    return []


def save_user_paths(user_paths, user_paths_file):
    # Upewnij się, że katalog istnieje
    dir_path = os.path.dirname(user_paths_file)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(user_paths_file, "w") as f:
        json.dump(user_paths, f, indent=2)
