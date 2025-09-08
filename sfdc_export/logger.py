import os
from datetime import datetime
from sfdc_export import config

def log(message: str):
    os.makedirs(config.SFDC_DIRECTORY, exist_ok=True)
    log_file = os.path.join(config.SFDC_DIRECTORY, "bulk_extraction.log")
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} {message}"
    print(entry)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry + "\n")