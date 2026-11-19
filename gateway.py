import serial
import struct
import zlib
import time

from gps.gps_handler import decode_gps
from storage.beacon_storage import save_beacon, load_beacons
from uplink.message_queue import queue_message
from uplink.retry import retry_pending_messages

latest = load_beacons()
print(f"Loaded saved beacons: {latest}")

ser = serial.Serial("/tmp/ttyB", 115200, timeout=1)

last_retry = 0
retry_interval = 5
buffer = b""

while True:

    if time.monotonic() - last_retry >= retry_interval:
        retry_pending_messages()
        last_retry = time.monotonic()

    buffer += ser.read(33 - len(buffer))

    if len(buffer) < 33:
        continue

    frame = buffer[:33]
    buffer = buffer[33:]

    payload = frame[:29]
    crc = struct.unpack(">I", frame[29:])[0]

    if zlib.crc32(payload) != crc:
        print("DROP bad CRC")
        continue

    beacon_id, seq = struct.unpack(">HH", payload[:4])

    if seq <= latest.get(beacon_id, -1):
        print(f"DROP duplicate/old: beacon {beacon_id} seq {seq}")
        continue

    latest[beacon_id] = seq
    print(f"OK beacon {beacon_id} seq {seq}")

    gps = decode_gps(payload)

    if gps is not None:
        latitude = gps["latitude"]
        longitude = gps["longitude"]
        print(f"GPS coordinates: {latitude}, {longitude}")
    else:
        latitude = None
        longitude = None
        print("GPS coordinates unavailable")

    queue_message(beacon_id, seq, latitude, longitude)

    save_beacon(beacon_id, seq, payload)
