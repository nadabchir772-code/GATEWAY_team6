import json
import os

FILE = "storage/beacons.json"
BACKUP_FILE = "storage/beacons_backup.json"

def save_beacon(beacon_id, seq, payload=None):
    data = {}

    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            data = json.load(f)

    data[str(beacon_id)] = {"seq": seq, "payload_hex": payload.hex() if payload is not None else None}

    temp_file = FILE + ".tmp"

    with open(temp_file, "w") as f:
        json.dump(data, f, indent=4)
        f.flush()
        os.fsync(f.fileno())

    os.replace(temp_file, FILE)

    backup_temp = BACKUP_FILE + ".tmp"
    with open(backup_temp, "w") as f:
        json.dump(data, f, indent=4)
        f.flush()
        os.fsync(f.fileno())

    os.replace(backup_temp, BACKUP_FILE)

    print(f"SAVED beacon {beacon_id} seq {seq}")


def load_beacons():
    for filename in (FILE, BACKUP_FILE):
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            result = {
                int(beacon_id): info["seq"]
                for beacon_id, info in data.items()
            }
            print(f"Loaded beacon data from {filename}")
            return result

        except (OSError, ValueError, TypeError, KeyError) as error:
            print(f"Cannot load {filename}: {error}")

    print("WARNING: No valid beacon storage found")
    return {}
