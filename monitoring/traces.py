import json
from datetime import datetime

def log_event(event_type: str, data: dict):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "data": data
    }

    with open("monitoring/trace.log", "a") as f:
        f.write(json.dumps(record) + "\n")
