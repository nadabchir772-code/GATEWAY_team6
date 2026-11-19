# LivingMap Phase 2 - Team 6 Gateway

## 1. Project Overview

The Gateway receives beacon data, validates messages,
extracts GPS coordinates, stores data locally and
transmits information to a remote server using TCP.

The Gateway also supports offline message storage
and automatic retransmission after network recovery.

## 2. Implemented Features

- Serial communication (UART simulation)
- Beacon frame reception
- CRC32 integrity verification
- Duplicate and old message detection
- Persistent JSON storage
- GPS decoding and validation
- TCP uplink communication
- Receiver acknowledgment (ACK)
- Persistent offline message queue
- Automatic retries every 5 seconds
- Automatic network recovery

## 3. System Architecture

Beacon
  |
  v
Serial Communication
  |
  v
Gateway
  |
  v
CRC and Sequence Validation
  |
  v
GPS Decoding
  |
  v
Local Storage and Message Queue
  |
  v
TCP Uplink
  |
  v
Server / Receiver
  |
  v
ACK Confirmation

## 4. Project Structure

gateway/
    gateway.py
    fake_beacon.py
    fake_beacon_gps.py
    gps/
        gps_handler.py
    storage/
        beacon_storage.py
        beacons.json
        beacons_backup.json
    uplink/
        sender.py
        receiver.py
        message_queue.py
        retry.py
        queue/
    README.md

## 5. Technologies

- Ubuntu Linux
- Python 3
- PySerial
- Socat
- TCP/IP
- JSON
- CRC32

## 6. Execution Instructions

Terminal 1 - TCP Receiver:

    cd ~/gateway
    python3 uplink/receiver.py

Terminal 3 - Serial Simulation:

    socat -d -d PTY,link=/tmp/ttyA,raw,echo=0 PTY,link=/tmp/ttyB,raw,echo=0

Terminal 2 - Gateway:

    cd ~/gateway
    python3 gateway.py

Terminal 4 - GPS Beacon Simulator:

    cd ~/gateway
    python3 fake_beacon_gps.py

The simulator starting sequence number must be
higher than the last saved beacon sequence number.

## 7. Test Results

- Serial communication: PASSED
- CRC validation: PASSED
- Duplicate detection: PASSED
- Persistent storage: PASSED
- GPS decoding: PASSED
- TCP transmission: PASSED
- ACK confirmation: PASSED
- Offline message storage: PASSED
- Automatic retries: PASSED
- Network outage simulation: PASSED
- Automatic network recovery: PASSED
- Final empty queue verification: PASSED

## 8. Network Failure Management

Messages are saved locally before transmission.

If the server is unavailable, messages remain
in the persistent queue.

The Gateway periodically retries pending messages.

After receiving an ACK, the acknowledged message
is removed from the queue.

This mechanism is called Store and Forward.

## 9. Current Limitations

The system has been tested in a local simulation.

Real hardware integration and communication with
the other teams remain to be validated.

The simulated GPS frame format must be confirmed
with the beacon team.

ACK confirms JSON reception and decoding, not
permanent storage on the remote server.

Exactly-once delivery is not guaranteed.

## 10. Conclusion

Team 6 successfully implemented and locally tested
a Gateway supporting beacon reception, validation,
GPS processing, persistent storage, TCP transmission
and automatic network recovery.
