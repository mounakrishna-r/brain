# core/logger.py (Updated)

import os
import json
import csv
from datetime import datetime

LOG_FILE = "data/memory_log.json"
os.makedirs("data", exist_ok=True)

def log_conversation(user_input, response):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "virus_response": response
    }

    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []
    except json.JSONDecodeError:
        data = []

    data.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def clear_log():
    with open(LOG_FILE, "w") as f:
        json.dump([], f)
    print(f"[🧹] Cleared: {LOG_FILE}")

def export_log_to_csv(csv_path="data/memory_log.csv"):
    if not os.path.exists(LOG_FILE):
        print("[!] No log file to export.")
        return

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "user_input", "virus_response"])
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

    print(f"[📁] Log exported to: {csv_path}")
