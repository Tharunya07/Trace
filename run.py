# run.py

import threading
import time
import main  # runs the Trace engine loop
from dashboard.app import run_dashboard  # to be created soon

def start_Trace():
    main.main()

def start_dashboard():
    run_dashboard()

if __name__ == "__main__":
    print("🚀 Starting Trace...")

    # Start Trace Monitor in background
    Trace_thread = threading.Thread(target=start_Trace, daemon=True)
    Trace_thread.start()

    # Optional: wait for it to stabilize
    time.sleep(1)

    # Start dashboard in main thread
    start_dashboard()
