import os

STATS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stats.log")


def load_stats():
    """Loads the total downloaded MB from stats.log file."""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            try:
                mb = float(f.read().strip())
                return mb
            except Exception:
                return 0.0
    return 0.0


def save_stats(mb):
    """Saves the total downloaded MB to stats.log file."""
    with open(STATS_FILE, "w") as f:
        f.write(f"{mb:.2f}")


def add_to_stats(bytes_downloaded):
    """Adds the size of the newly downloaded file to the total MB and updates stats.log."""
    mb_downloaded = bytes_downloaded / (1024 * 1024)
    current = load_stats()
    total = current + mb_downloaded
    save_stats(total)
    return total
