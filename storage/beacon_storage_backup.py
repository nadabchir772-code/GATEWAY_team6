import json
import os

FILE = "storage/beacons.json"

def save_beacon(beacon_id, seq):
    data = {}

    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            data = json.load(f)

    data[str(beacon_id)] = {"seq": seq}

    temp_file = FILE + ".tmp"

    with open(temp_file, "w") as f:
        json.dump(data, f, indent=4)
        f.flush()
        os.fsync(f.fileno())

    os.replace(temp_file, FILE)

    print(f"SAVED beacon {beacon_id} seq {seq}")


def load_beacons():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        data = json.load(f)
    return {int(beacon_id): info["seq"] for beacon_id, info in data.items()}
