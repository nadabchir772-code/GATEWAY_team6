import serial
import struct
import time
import zlib

def make_frame(beacon_id, seq, latitude, longitude):
    # Temporary GPS simulation format
    payload = struct.pack(
        ">HHdd",
        beacon_id,
        seq,
        latitude,
        longitude
    ) + bytes(9)

    crc = zlib.crc32(payload)
    return payload + struct.pack(">I", crc)


ser = serial.Serial("/tmp/ttyA", 115200)
seq = 739

while True:
    seq += 1

    frame = make_frame(1, seq, 36.8, 10.18)
    ser.write(frame)

    print(f"Sent GPS beacon seq {seq}")
    time.sleep(1)
