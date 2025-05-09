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
    os.path.abspath(
        os.path.join(__file__, "..", "..", "..", "..", "..", "Pobrane", "youtube")
    ),
)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def should_log(level):
    levels = {"ERROR": 0, "WARNING": 1, "INFO": 2}
    return levels.get(level, 2) <= levels.get(LOG_LEVEL, 2)


def log_event(message, level="INFO"):
    if not should_log(level):
        return
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}\n"
    with open(log_file, "a") as f:
        f.write(entry)
    # You can also print the log entry to the console:
    # print(entry, end="")


def check_free_space(directory, min_bytes=500 * 1024 * 1024):
    """Checks if there is at least min_bytes of free space in the directory (default 500MB)."""
    stat = os.statvfs(directory)
    free = stat.f_bavail * stat.f_frsize
    return free >= min_bytes, free


def save_url_if_new(url):
    adres_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "adres.txt")
    # Load existing URLs (one per line)
    if os.path.exists(adres_file):
        with open(adres_file, "r") as f:
            urls = set(line.strip() for line in f if line.strip())
    else:
        urls = set()
    # Add only if not already present
    if url not in urls:
        with open(adres_file, "a") as f:
            f.write(url + "\n")
        log_event(f"Added new URL to adres.txt: {url}", level="INFO")
    else:
        log_event(f"URL already exists in adres.txt: {url}", level="INFO")


def main():
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
        except Exception as e:
            log_event(f"Error during download: {e}", level="ERROR")
            print("An error occurred during download. See log for details.")
            continue

        if file_path:
            # Count the size of the downloaded file
            try:
                size_bytes = os.path.getsize(file_path)
                total_mb = add_to_stats(size_bytes)
                log_event(
                    f"Stats updated: total downloaded {total_mb:.2f} MB",
                    level="INFO",
                )
            except Exception as e:
                log_event(f"Failed to update stats: {e}", level="WARNING")
            log_event(f"Downloaded: {file_path}")
            user_paths = load_user_paths(USER_PATHS_FILE)
            if DOWNLOAD_PATH and DOWNLOAD_PATH not in user_paths:
                user_paths.insert(0, DOWNLOAD_PATH)
                save_user_paths(user_paths, USER_PATHS_FILE)
            copy_to(file_path, USER_PATHS_FILE)
            log_event(f"Copied to selected location: {file_path}")
            if os.path.exists(file_path):
                delete_file(file_path)
                log_event(f"Deleted file: {file_path}")
            else:
                log_event(f"File not found for deletion: {file_path}", level="WARNING")
        save_url_if_new(url)
        again = input("Do you want to download another file? (y/n): ").strip().lower()
        if again != "y":
            print("Program finished.")
            break


if __name__ == "__main__":
    main()
