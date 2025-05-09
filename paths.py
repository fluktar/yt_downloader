import json
from os import path


def load_user_paths(user_paths_file):
    if path.exists(user_paths_file):
        with open(user_paths_file, "r") as f:
            return json.load(f)
    return []


def save_user_paths(paths, user_paths_file):
    with open(user_paths_file, "w") as f:
        json.dump(paths, f)
