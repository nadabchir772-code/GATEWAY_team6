from gps.gps_handler import decode_gps
import serial, struct, zlib
from storage.beacon_storage import save_beacon, load_beacons
latest = load_beacons()
print(f"Loaded saved beacons: {latest}")

ser = serial.Serial("/tmp/ttyB", 115200)
while True:
    frame = ser.read(33)
    payload, crc = frame[:29], struct.unpack(">I", frame[29:])[0]
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
        print(f"GPS coordinates: {gps['latitude']}, {gps['longitude']}")
    else:
        print("GPS coordinates unavailable")

    save_beacon(beacon_id, seq, payload)
