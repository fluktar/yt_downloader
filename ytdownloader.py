import os
import json
from downloader import download_video
from paths import load_user_paths, save_user_paths
from fileops import copy_to, delete_file
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

USER_PATHS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "user_paths.json"
)

DOWNLOAD_PATH = os.path.abspath(
    os.path.join(__file__, "..", "..", "..", "..", "..", "Pobrane", "youtube")
)


def log_event(message):
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def check_free_space(directory, min_bytes=500 * 1024 * 1024):
    """Sprawdza, czy w katalogu jest co najmniej min_bytes wolnego miejsca (domyślnie 500MB)."""
    stat = os.statvfs(directory)
    free = stat.f_bavail * stat.f_frsize
    return free >= min_bytes, free


def main():
    while True:
        url_input = input(
            "Podaj link do filmu (pozostaw puste, aby użyć domyślnego): "
        ).strip()
        url = url_input if url_input else "https://www.youtube.com/watch?v=tCDvOQI3pco"

        typ = input("Co chcesz pobrać? [1] Wideo [2] Tylko audio: ").strip()
        only_audio = typ == "2"

        ok, free = check_free_space(DOWNLOAD_PATH)
        if not ok:
            print(
                f"Za mało wolnego miejsca w {DOWNLOAD_PATH} ({free // (1024*1024)} MB). Pobieranie anulowane."
            )
            log_event(f"Za mało miejsca: {free} bajtów w {DOWNLOAD_PATH}")
            continue

        file_path = download_video(url, DOWNLOAD_PATH, only_audio=only_audio)
        if file_path:
            log_event(f"Pobrano: {file_path}")
            copy_to(file_path, USER_PATHS_FILE)
            log_event(f"Skopiowano do wybranej lokalizacji: {file_path}")
            delete_file(file_path)
            log_event(f"Usunięto plik: {file_path}")
        again = input("Czy chcesz pobrać kolejny plik? (t/n): ").strip().lower()
        if again != "t":
            print("Koniec programu.")
            break


if __name__ == "__main__":
    main()
