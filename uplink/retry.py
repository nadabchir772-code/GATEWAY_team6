from pathlib import Path
from uplink.sender import send_beacon
from uplink.message_queue import get_pending_messages


def retry_pending_messages():
    for item in get_pending_messages():
        message = item["message"]
        filename = Path(item["filename"])

        success = send_beacon(
            message["beacon_id"],
            message["seq"],
            message["latitude"],
            message["longitude"]
        )

        if success:
            filename.unlink()
            print(f"QUEUE CLEARED: {filename.name}")
        else:
            print(f"RETRY FAILED: {filename.name}")
            break
