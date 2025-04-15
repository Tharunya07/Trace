# report.py

import sqlite3
from datetime import datetime, timedelta

DB_PATH = "db/Trace.db"

def get_daily_report():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    query = """
        SELECT ip, COUNT(*) as count 
        FROM events 
        WHERE type='FAIL' AND timestamp LIKE ? 
        GROUP BY ip 
        ORDER BY count DESC
    """

    c.execute(query, (f"{today}%",))
    results = c.fetchall()
    conn.close()

    print(f"\n[Daily Summary - {today}]")
    print(f"Total Brute Force Alerts: {len(results)}")
    for ip, count in results:
        print(f"IP: {ip} | Failed Attempts: {count}")

if __name__ == "__main__":
    get_daily_report()
