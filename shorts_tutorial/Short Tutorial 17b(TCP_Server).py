# TCP - Server
import network
from machine import SPI, Pin
import socket

# Setup
spi = SPI(2, baudrate=8_000_000)
nic = network.WIZNET5K(spi, Pin("PB12", Pin.OUT), Pin("PD9", Pin.OUT))
nic.active(True)
nic.ifconfig(("192.168.1.20", "255.255.255.0", "192.168.1.1", "8.8.8.8"))

# Echo server
s = socket.socket()
s.bind(("192.168.1.20", 5000))
s.listen(1)
print("Echo server running...")

conn, addr = s.accept()
print("Client connected")
while True:
    data = conn.recv(1024)
    if data == b"exit":
        break
    conn.send(b"Echo: " + data)
conn.close()