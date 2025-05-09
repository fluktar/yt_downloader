import os
from os import path, remove, makedirs
from shutil import copy
from paths import load_user_paths, save_user_paths


def get_predefined_paths():
    paths = os.getenv("PREDEFINED_PATHS", "")
    return [p.strip() for p in paths.split(",") if p.strip()]


def copy_to(file_path, user_paths_file):
    predefined_paths = get_predefined_paths()

    while True:
        user_paths = load_user_paths(user_paths_file)
        all_paths = predefined_paths + user_paths
        print("Wybierz miejsce docelowe:")
        for i, p in enumerate(all_paths, 1):
            print(f"{i} - {p}")
        print(f"{len(all_paths)+1} - Dodaj nową ścieżkę")
        print(f"{len(all_paths)+2} - Usuń ścieżkę użytkownika")
        print(f"{len(all_paths)+3} - Anuluj")

        try:
            choice = int(input("Twój wybór: ").strip())
        except ValueError:
            print("Nieprawidłowy wybór. Operacja kopiowania anulowana.")
            return

        if 1 <= choice <= len(all_paths):
            copy_path = all_paths[choice - 1]
            if not path.exists(copy_path):
                print(
                    f"Ścieżka {copy_path} nie istnieje. Upewnij się, że podałeś poprawną ścieżkę."
                )
                return
            try:
                destination_path = path.join(copy_path, path.basename(file_path))
                print(f"Ścieżka źródłowa: {file_path}")
                print(f"Ścieżka docelowa: {destination_path}")
                copy(file_path, destination_path)
                print(f"Skopiowano do: {destination_path}")
            except Exception as e:
                print(f"Wystąpił błąd podczas kopiowania pliku: {e}")
            return

        elif choice == len(all_paths) + 1:
            new_path = input("Podaj nową ścieżkę do dodania: ").strip()
            print(f"DEBUG: Dodajesz ścieżkę: {new_path}")
            print(f"DEBUG: user_paths przed dodaniem: {user_paths}")
            if new_path and new_path not in user_paths:
                if not path.exists(new_path):
                    create = (
                        input("Katalog nie istnieje. Utworzyć? (t/n): ").strip().lower()
                    )
                    if create == "t":
                        try:
                            makedirs(new_path)
                            print("Katalog został utworzony.")
                        except Exception as e:
                            print(f"Nie udało się utworzyć katalogu: {e}")
                            continue
                    else:
                        print("Nie dodano ścieżki.")
                        continue
                user_paths.append(new_path)
                save_user_paths(user_paths, user_paths_file)
                print("Dodano nową ścieżkę.")
            else:
                print("Nieprawidłowa lub już istniejąca ścieżka.")

        elif choice == len(all_paths) + 2:
            if not user_paths:
                print("Brak ścieżek użytkownika do usunięcia.")
                continue
            print("Wybierz numer ścieżki użytkownika do usunięcia:")
            for i, p in enumerate(user_paths, 1):
                print(f"{i} - {p}")
            try:
                del_choice = int(input("Twój wybór: ").strip())
                if 1 <= del_choice <= len(user_paths):
                    removed = user_paths.pop(del_choice - 1)
                    save_user_paths(user_paths, user_paths_file)
                    print(f"Usunięto ścieżkę: {removed}")
                else:
                    print("Nieprawidłowy wybór.")
            except ValueError:
                print("Nieprawidłowy wybór.")

        elif choice == len(all_paths) + 3:
            print("Operacja kopiowania anulowana.")
            return
        else:
            print("Nieprawidłowy wybór.")


def delete_file(file_path):
    """
    Usuwa plik z katalogu Pobrane/youtube.

    :param file_path: Ścieżka do pliku do usunięcia
    """
    if not file_path or not path.exists(file_path):
        print("Plik nie istnieje lub ścieżka jest nieprawidłowa.")
        return

    try:
        remove(file_path)
        print(f"Usunięto: {file_path}")
    except Exception as e:
        print(f"Wystąpił błąd podczas usuwania pliku: {e}")
