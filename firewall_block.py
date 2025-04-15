# firewall_block.py

import subprocess
import sys

def block_ip(ip):
    try:
        cmd = ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
        subprocess.run(cmd, check=True)
        print(f"🚫 Blocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to block IP: {ip}\n{e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python firewall_block.py <IP_ADDRESS>")
    else:
        block_ip(sys.argv[1])
