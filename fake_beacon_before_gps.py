import serial, struct, time, zlib, random

def make_frame(beacon_id, seq):
    payload = struct.pack(">HH", beacon_id, seq) + bytes(25)
    return payload + struct.pack(">I", zlib.crc32(payload))

ser = serial.Serial("/tmp/ttyA", 115200)
seq = 0
while True:
    seq += 1
    frame = make_frame(1, seq)
    if random.random() < 0.2:
        frame = frame[:5] + b"\xff" + frame[6:]
    ser.write(frame)
    if random.random() < 0.3:
        ser.write(frame)
    time.sleep(1)
