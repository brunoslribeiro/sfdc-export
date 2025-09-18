import os
from datetime import datetime

LOG_DIRECTORY = "./output"


def set_log_directory(path: str):
    """Configure where log files are written."""
    global LOG_DIRECTORY
    LOG_DIRECTORY = path


def log(message: str):
    os.makedirs(LOG_DIRECTORY, exist_ok=True)
    log_file = os.path.join(LOG_DIRECTORY, "bulk_extraction.log")
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} {message}"
    print(entry)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry + "\n")