import network
import time
from machine import SPI, Pin
import socket
import uerrno as errno

NET_IP   = "192.168.1.20"
NET_SN   = "255.255.255.0"
NET_GW   = "192.168.1.1"
NET_DNS  = "8.8.8.8"

DEST_IP = "192.168.1.100"
DEST_PORT = 5000

spi = SPI(2, baudrate=8_000_000, polarity=0, phase=0)

cs  = Pin("PB12", Pin.OUT)
rst = Pin("PD9", Pin.OUT)
pwn = Pin("PE15", Pin.OUT, value = 0)

nic = network.WIZNET5K(spi, cs, rst)
nic.active(True)
nic.ifconfig((NET_IP, NET_SN, NET_GW, NET_DNS))

ip, subnet, gateway, dns = nic.ifconfig()
print("IP address of W55MH32L-EVB :", ip)
s=socket.socket()
print("Connecting to {}:{}".f /ormat(DEST_IP, DEST_PORT))
s.connect((DEST_IP, DEST_PORT))

# Send test messages
for msg in [b"Hello\n", b"World\n", b"Test\n", b"exit\n"]:
    s.send(msg)
    if msg != b"exit\n":
        response = s.recv(1024)
        print(f"Received: {response.decode().strip()}")

s.close()
print("Connection closed")

