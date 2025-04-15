from flask import Flask, render_template, request, redirect, url_for, session, send_file
from functools import wraps
import sqlite3
import io
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"  # change in production
DB_PATH = "db/Trace.db"

# Load config
with open("config.json") as f:
    config = json.load(f)

# Auth wrapper
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (request.form["username"] == config["dashboard_user"] and
            request.form["password"] == config["dashboard_pass"]):
            session["logged_in"] = True
            return redirect(url_for("index"))
        return "Invalid credentials", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    selected_date = request.args.get("date") or datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT ip, COUNT(*) FROM events
        WHERE type='FAIL' AND timestamp LIKE ?
        GROUP BY ip ORDER BY COUNT(*) DESC LIMIT 5
    """, (f"{selected_date}%",))
    top_ips = c.fetchall()

    c.execute("""
        SELECT strftime('%H', timestamp) as hour, COUNT(*) FROM events
        WHERE type='FAIL' AND timestamp LIKE ?
        GROUP BY hour ORDER BY hour
    """, (f"{selected_date}%",))
    timeline = c.fetchall()

    c.execute("""
        SELECT COUNT(*) FROM events
        WHERE type='SUCCESS' AND timestamp LIKE ?
    """, (f"{selected_date}%",))
    success_count = c.fetchone()[0]

    conn.close()

    ip_labels = [ip for ip, _ in top_ips]
    ip_data = [count for _, count in top_ips]
    timeline_labels = [f"{hour}:00" for hour, _ in timeline]
    timeline_data = [count for _, count in timeline]

    return render_template("index.html",
        selected_date=selected_date,
        ip_labels=ip_labels,
        ip_data=ip_data,
        timeline_labels=timeline_labels,
        timeline_data=timeline_data,
        top_ips=top_ips,
        success_count=success_count
    )

@app.route("/export")
@login_required
def export_csv():
    selected_date = request.args.get("date") or datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT timestamp, ip, user, type FROM events
        WHERE timestamp LIKE ? ORDER BY timestamp
    """, (f"{selected_date}%",))
    rows = c.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Timestamp", "IP", "User", "Type"])
    writer.writerows(rows)
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f"Trace_report_{selected_date}.csv"
    )

def run_dashboard():
    app.run(debug=True, port=5000)
