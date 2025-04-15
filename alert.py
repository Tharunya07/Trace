# alert.py

from firewall_block import block_ip
import json
import platform

# Load config
with open("config.json") as f:
    config = json.load(f)

AUTO_BLOCK = config.get("auto_block_enabled", False)

def send_alert(ip, count, start_time, end_time):
    print(f"\n[⚠️ ALERT] Possible Brute-Force Attack!")
    print(f"IP: {ip} | {count} failed attempts between {start_time} and {end_time}\n")

    with open("logs/alert_log.txt", "a") as f:
        f.write(f"[{end_time}] ALERT: Brute force from {ip} ({count} attempts)\n")

    if AUTO_BLOCK:
        if platform.system() == "Windows":
            print(f"⚠️ Windows detected — skipping IP block for {ip} (iptables not supported)")
        else:
            block_ip(ip)
