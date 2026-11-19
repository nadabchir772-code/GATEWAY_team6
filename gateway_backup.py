import serial, struct, zlib

latest = {}

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
