# parser.py

import re
from datetime import datetime

# Regex patterns for various service logs
SSH_FAIL = r"Failed password for( invalid user)? (?P<user>\w+) from (?P<ip>[0-9.]+)"
SSH_SUCCESS = r"Accepted password for (?P<user>\w+) from (?P<ip>[0-9.]+)"
FTP_FAIL = r"FTP login failed.*from (?P<ip>[0-9.]+)"
MYSQL_FAIL = r"MySQL.*Access denied for user '(?P<user>[^']+)'@(?P<ip>[0-9.]+)"

def parse_log_line(line):
    timestamp = datetime.now()

    if "sshd" in line:
        fail_match = re.search(SSH_FAIL, line)
        if fail_match:
            return {"type": "FAIL", "user": fail_match.group("user"), "ip": fail_match.group("ip"), "timestamp": timestamp}
        
        success_match = re.search(SSH_SUCCESS, line)
        if success_match:
            return {"type": "SUCCESS", "user": success_match.group("user"), "ip": success_match.group("ip"), "timestamp": timestamp}

    ftp_match = re.search(FTP_FAIL, line)
    if ftp_match:
        return {"type": "FAIL", "user": "unknown", "ip": ftp_match.group("ip"), "timestamp": timestamp}

    mysql_match = re.search(MYSQL_FAIL, line)
    if mysql_match:
        return {"type": "FAIL", "user": mysql_match.group("user"), "ip": mysql_match.group("ip"), "timestamp": timestamp}

    return None
