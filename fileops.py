import os
from os import path, remove, makedirs
from shutil import copy
from paths import load_user_paths, save_user_paths


def get_predefined_paths():
    # Reads predefined paths from environment variable
    paths = os.getenv("PREDEFINED_PATHS", "")
    return [p.strip() for p in paths.split(",") if p.strip()]


def copy_to(file_path, user_paths_file):
    """
    Allows user to select a destination directory for the file.
    Supports adding and removing custom user paths.
    """
    predefined_paths = get_predefined_paths()

    while True:
        user_paths = load_user_paths(user_paths_file)
        all_paths = predefined_paths + user_paths
        print("Select destination:")
        for i, p in enumerate(all_paths, 1):
            print(f"{i} - {p}")
        print(f"{len(all_paths)+1} - Add new path")
        print(f"{len(all_paths)+2} - Remove user path")
        print(f"{len(all_paths)+3} - Cancel")

        try:
            choice = int(input("Your choice: ").strip())
        except ValueError:
            print("Invalid choice. Copy operation canceled.")
            return

        if 1 <= choice <= len(all_paths):
            copy_path = all_paths[choice - 1]
            if not path.exists(copy_path):
                print(
                    f"Path {copy_path} does not exist. Please make sure you entered a valid path."
                )
                return
            try:
                destination_path = path.join(copy_path, path.basename(file_path))
                print(f"Source path: {file_path}")
                print(f"Destination path: {destination_path}")
                copy(file_path, destination_path)
                print(f"Copied to: {destination_path}")
            except Exception as e:
                print(f"Error while copying file: {e}")
            return

        elif choice == len(all_paths) + 1:
            new_path = input("Enter new path to add: ").strip()
            if new_path and new_path not in user_paths:
                if not path.exists(new_path):
                    create = (
                        input("Directory does not exist. Create it? (y/n): ")
                        .strip()
                        .lower()
                    )
                    if create == "y":
                        try:
                            makedirs(new_path)
                            print("Directory created.")
                        except Exception as e:
                            print(f"Failed to create directory: {e}")
                            continue
                    else:
                        print("Path not added.")
                        continue
                user_paths.append(new_path)
                save_user_paths(user_paths, user_paths_file)
                print("New path added.")
            else:
                print("Invalid or already existing path.")

        elif choice == len(all_paths) + 2:
            if not user_paths:
                print("No user paths to remove.")
                continue
            print("Select user path number to remove:")
            for i, p in enumerate(user_paths, 1):
                print(f"{i} - {p}")
            try:
                del_choice = int(input("Your choice: ").strip())
                if 1 <= del_choice <= len(user_paths):
                    removed = user_paths.pop(del_choice - 1)
                    save_user_paths(user_paths, user_paths_file)
                    print(f"Removed path: {removed}")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid choice.")

        elif choice == len(all_paths) + 3:
            print("Copy operation canceled.")
            return
        else:
            print("Invalid choice.")


def delete_file(file_path):
    """Deletes the specified file if it exists."""
    if path.exists(file_path):
        try:
            remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Wystąpił błąd podczas usuwania pliku: {e}")
    else:
        print("File does not exist or invalid path.")
