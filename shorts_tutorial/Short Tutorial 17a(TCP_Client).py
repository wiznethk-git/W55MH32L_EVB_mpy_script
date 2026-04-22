# TCP - Client
import network
from machine import SPI, Pin
import socket

spi = SPI(2, baudrate=8_000_000)
nic = network.WIZNET5K(spi, Pin("PB12", Pin.OUT), Pin("PD9", Pin.OUT))
nic.active(True)
nic.ifconfig(("192.168.1.21", "255.255.255.0", "192.168.1.1", "8.8.8.8"))

s = socket.socket()
s.connect(("192.168.1.20", 5000))

# Send test messages
for msg in [b"Hello", b"World", b"Test", b"exit"]:
    s.send(msg)
    if msg != b"exit":
        print(s.recv(1024).decode())
s.close()