import math
import struct

def validate_gps(latitude, longitude):
    if latitude is None or longitude is None:
        return False
    if not isinstance(latitude, (int, float)):
        return False
    if not isinstance(longitude, (int, float)):
        return False
    if not math.isfinite(latitude) or not math.isfinite(longitude):
        return False
    if not (-90 <= latitude <= 90):
        return False
    if not (-180 <= longitude <= 180):
        return False
    return True

def decode_gps(payload):
    if len(payload) != 29:
        return None
    latitude, longitude = struct.unpack(">dd", payload[4:20])
    if not validate_gps(latitude, longitude):
        return None
    return {"latitude": latitude, "longitude": longitude}
