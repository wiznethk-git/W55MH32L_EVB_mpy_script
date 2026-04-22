# UDP - Client

import network
from machine import SPI, Pin
import socket

spi = SPI(2, baudrate=8_000_000)
nic = network.WIZNET5K(spi, Pin("PB12", Pin.OUT), Pin("PD9", Pin.OUT))
nic.active(True)
nic.ifconfig(("192.168.1.21", "255.255.255.0", "192.168.1.1", "8.8.8.8"))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg = input("Message: ")
    if not msg:
        break
    s.sendto(msg.encode(), ("192.168.1.20", 5000))
    data, addr = s.recvfrom(1024)
    print(data.decode())

s.close()