import socket
import json

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print(f"Uplink receiver listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"Connected: {addr}")

    with conn:
        buffer = b""

        while True:
            data = conn.recv(1024)

            if not data:
                break

            buffer += data

            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)

                try:
                    message = json.loads(line.decode("utf-8"))
                    print(f"RECEIVED: {message}")
                    conn.sendall(b"ACK\n")
                except (ValueError, UnicodeDecodeError):
                    print("Invalid message received")
