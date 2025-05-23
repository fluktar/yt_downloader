import os
import json
from downloader import download_video
from paths import load_user_paths, save_user_paths
from fileops import copy_to, delete_file
from dotenv import load_dotenv
from datetime import datetime
from stats import add_to_stats, load_stats

load_dotenv()

USER_PATHS_FILE = os.getenv(
    "USER_PATHS_FILE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_paths.json"),
)

DOWNLOAD_PATH = os.getenv(
    "DOWNLOAD_PATH",
    os.path.expanduser("~/Pobrane/youtube"),
)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_file_path(filename):
    return os.path.join(BASE_DIR, filename)


def should_log(level):
    levels = {"ERROR": 0, "WARNING": 1, "INFO": 2}
    return levels.get(level, 2) <= levels.get(LOG_LEVEL, 2)


def log_event(message, level="INFO"):
    if not should_log(level):
        return
    log_file = get_file_path("log.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}\n"
    with open(log_file, "a") as f:
        f.write(entry)


def check_free_space(directory, min_bytes=500 * 1024 * 1024):
    """Checks if there is at least min_bytes of free space in the directory (default 500MB)."""
    stat = os.statvfs(directory)
    free = stat.f_bavail * stat.f_frsize
    return free >= min_bytes, free


def save_url_if_new(url):
    adres_file = get_file_path("adres.txt")
    if os.path.exists(adres_file):
        with open(adres_file, "r") as f:
            urls = set(line.strip() for line in f if line.strip())
    else:
        urls = set()
    if url not in urls:
        with open(adres_file, "a") as f:
            f.write(url + "\n")
        log_event(f"Added new URL to adres.txt: {url}", level="INFO")
    else:
        log_event(f"URL already exists in adres.txt: {url}", level="INFO")


def main():
    print(f"DOWNLOAD_PATH is set to: {DOWNLOAD_PATH}")
    log_event(f"DOWNLOAD_PATH is set to: {DOWNLOAD_PATH}", level="INFO")

    if not os.path.exists(DOWNLOAD_PATH):
        print(f"DOWNLOAD_PATH does not exist. Creating: {DOWNLOAD_PATH}")
        os.makedirs(DOWNLOAD_PATH)
        log_event(f"Created missing download directory: {DOWNLOAD_PATH}", level="INFO")
    else:
        print(f"DOWNLOAD_PATH exists: {DOWNLOAD_PATH}")
        log_event(f"DOWNLOAD_PATH exists: {DOWNLOAD_PATH}", level="INFO")

    total_mb = load_stats()
    print(f"Total downloaded so far: {total_mb:.2f} MB")

    user_paths = load_user_paths(USER_PATHS_FILE)
    if DOWNLOAD_PATH and DOWNLOAD_PATH not in user_paths:
        user_paths.insert(0, DOWNLOAD_PATH)
        save_user_paths(user_paths, USER_PATHS_FILE)

    while True:
        url_input = input("Enter video link (leave empty to use the default): ").strip()
        url = url_input if url_input else "https://www.youtube.com/watch?v=tCDvOQI3pco"

        save_url_if_new(url)

        typ = input("What do you want to download? [1] Video [2] Audio only: ").strip()
        only_audio = typ == "2"

        ok, free = check_free_space(DOWNLOAD_PATH)
        if not ok:
            print(
                f"Not enough free space in {DOWNLOAD_PATH} ({free // (1024*1024)} MB). Download canceled."
            )
            log_event(
                f"Not enough space: {free} bytes in {DOWNLOAD_PATH}", level="ERROR"
            )
            continue

        try:
            file_path = download_video(url, DOWNLOAD_PATH, only_audio=only_audio)
            if file_path is None:
                print("Download failed. Skipping.")
                log_event(
                    "Download returned None. Skipping post-download steps.",
                    level="WARNING",
                )
                continue
        except Exception as e:
            log_event(f"Failed to download: {e}", level="WARNING")
            continue

        log_event(f"Downloaded: {file_path}")

        copy_to(file_path, USER_PATHS_FILE)
        log_event(f"Copied to selected location: {file_path}")

        if os.path.exists(file_path):
            try:
                delete_file(file_path)
                log_event(f"Deleted file: {file_path}")
            except Exception as e:
                log_event(f"Failed to delete {file_path}: {e}", level="ERROR")
        else:
            log_event(f"File not found for deletion: {file_path}", level="WARNING")

        save_url_if_new(url)
        again = input("Do you want to download another file? (y/n): ").strip().lower()
        if again != "y":
            print("Program finished.")
            break


if __name__ == "__main__":
    main()
