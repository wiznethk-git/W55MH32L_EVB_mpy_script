# UDP - Server

import network
from machine import SPI, Pin
import socket

spi = SPI(2, baudrate=8_000_000)
nic = network.WIZNET5K(spi, Pin("PB12", Pin.OUT), Pin("PD9", Pin.OUT))
nic.active(True)
nic.ifconfig(("192.168.1.20", "255.255.255.0", "192.168.1.1", "8.8.8.8"))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("192.168.1.20", 5000))
print("UDP Echo Server Ready")

while True:
    data, addr = s.recvfrom(1024)
    print(f"{addr}: {data.decode()}")
    s.sendto(b"Echo: " + data, addr)