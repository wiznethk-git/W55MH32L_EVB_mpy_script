# TCP - Server
import network
import time
from machine import SPI, Pin
import socket

# Setup
NET_IP   = "192.168.1.20"
NET_SN   = "255.255.255.0"
NET_GW   = "192.168.1.1"
NET_DNS  = "8.8.8.8"
LOCAL_PORT  = 5000

DEST_IP = "192.168.1.100"

spi = SPI(2, baudrate=8_000_000, polarity=0, phase=0)
cs  = Pin("PB12", Pin.OUT)
rst = Pin("PD9", Pin.OUT)
pwn = Pin("PE15", Pin.OUT, value =0)

nic = network.WIZNET5K(spi, cs, rst)
nic.active(True)
nic.ifconfig((NET_IP, NET_SN, NET_GW, NET_DNS))

ip, subnet, gateway, dns = nic.ifconfig()
print("IP address of W55MH32L-EVB :", ip)

# Echo server
s = socket.socket()
s.bind((ip, LOCAL_PORT))
s.listen(1)
print("Echo server running...")

conn, addr = s.accept()
print(f"Client connected from {addr[0]}:{addr[1]}")
while True:
    data = conn.recv(1024)
    print(f"Received: {data.decode().strip()}")
    if data == b"exit":
        break
    conn.send(b"Echo: " + data +"\n")
conn.close()
