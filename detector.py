# detector.py

from datetime import datetime, timedelta
from collections import defaultdict
from alert import send_alert

class BruteForceDetector:
    def __init__(self, threshold=5, window=120):
        self.threshold = threshold
        self.window = timedelta(seconds=window)
        self.failed_logins = defaultdict(list)

    def process_event(self, event):
        if event["type"] != "FAIL":
            return

        ip = event["ip"]
        now = event["timestamp"]

        self.failed_logins[ip].append(now)

        # Remove old timestamps
        self.failed_logins[ip] = [
            t for t in self.failed_logins[ip] if now - t <= self.window
        ]

        if len(self.failed_logins[ip]) >= self.threshold:
            send_alert(ip, len(self.failed_logins[ip]), self.failed_logins[ip][0], now)
            self.failed_logins[ip] = []  # reset after alert
