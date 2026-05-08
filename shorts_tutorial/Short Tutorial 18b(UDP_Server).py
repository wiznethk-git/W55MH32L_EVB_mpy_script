# UDP Test - Server
import network
from machine import SPI, Pin
import socket
import time

NET_IP = "169.254.100.50"
DEST_IP = "169.254.219.97"
DEST_PORT = 5000

# Setup Ethernet
spi = SPI(2, baudrate=8_000_000)
cs = Pin("PB12", Pin.OUT)
rst = Pin("PD9", Pin.OUT)

nic = network.WIZNET5K(spi, cs, rst)
nic.active(True)
nic.ifconfig((NET_IP, "255.255.0.0", "0.0.0.0", "8.8.8.8"))

print(f"W55MH32L-EVB IP: {nic.ifconfig()[0]}")

# Create UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 5000))

while True:
    data, addr = s.recvfrom(1024)
    print(f"Response: {data.decode()}")
    if data.decode() == "exit":
        break

s.close()
print("Finished!")
