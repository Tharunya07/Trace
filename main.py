# main.py

import json
import time
from parser import parse_log_line
from detector import BruteForceDetector
from storage import save_event, init_db

# Load config
with open("config.json") as f:
    config = json.load(f)

LOG_FILE = config["log_path"]
THRESHOLD = config["threshold"]
TIME_WINDOW = config["time_window"]

# Initialize detector + DB
detector = BruteForceDetector(threshold=THRESHOLD, window=TIME_WINDOW)
init_db()

def tail_log(file_path):
    with open(file_path, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line.strip()

def main():
    print(f"🔍 Monitoring {LOG_FILE} ...")
    print(f"🛡️  Threshold: {THRESHOLD} failed attempts in {TIME_WINDOW} seconds")
    for line in tail_log(LOG_FILE):
        event = parse_log_line(line)
        if event:
            save_event(event)  # ⬅️ Save event to DB
            detector.process_event(event)

if __name__ == "__main__":
    main()
