import json
import os
from pathlib import Path

QUEUE_DIR = Path.home() / "gateway/uplink/queue"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)


def queue_message(beacon_id, seq, latitude, longitude):
    message = {
        "beacon_id": beacon_id,
        "seq": seq,
        "latitude": latitude,
        "longitude": longitude
    }

    filename = QUEUE_DIR / f"beacon_{beacon_id}_seq_{seq}.json"
    temp_filename = filename.with_suffix(".tmp")

    with open(temp_filename, "w") as f:
        json.dump(message, f)
        f.flush()
        os.fsync(f.fileno())

    os.replace(temp_filename, filename)

    print(f"QUEUED beacon {beacon_id} seq {seq}")
    return True


def get_pending_messages():
    messages = []

    for filename in sorted(QUEUE_DIR.glob("*.json")):
        try:
            with open(filename, "r") as f:
                message = json.load(f)

            messages.append({
                "filename": str(filename),
                "message": message
            })

        except (OSError, json.JSONDecodeError) as error:
            print(f"QUEUE READ ERROR: {error}")

    return messages
