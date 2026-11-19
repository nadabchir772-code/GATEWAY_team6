import socket
import json

HOST = "127.0.0.1"
PORT = 5000

def send_beacon(beacon_id, seq, latitude, longitude):
    message = {
        "beacon_id": beacon_id,
        "seq": seq,
        "latitude": latitude,
        "longitude": longitude
    }

    try:
        with socket.create_connection((HOST, PORT), timeout=3) as sock:
            data = json.dumps(message) + "\n"
            sock.sendall(data.encode("utf-8"))

        print(f"UPLINK SENT beacon {beacon_id} seq {seq}")
        return True

    except OSError as error:
        print(f"UPLINK ERROR: {error}")
        return False
