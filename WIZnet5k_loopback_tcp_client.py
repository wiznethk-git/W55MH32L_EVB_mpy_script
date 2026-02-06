import network
import time
from machine import SPI, Pin
import socket
import uerrno as errno

NET_IP   = "192.168.1.20"
NET_SN   = "255.255.255.0"
NET_GW   = "192.168.1.1"
NET_DNS  = "8.8.8.8"
LOCAL_PORT  = 5000

DEST_IP = "192.168.1.100"
DEST_PORT = 5001

spi = SPI(2, baudrate=8_000_000, polarity=0, phase=0)

cs  = Pin("PB12", Pin.OUT)
rst = Pin("PD9", Pin.OUT)
pwn = Pin("PE15", Pin.OUT, value =0)

nic = network.WIZNET5K(spi, cs, rst)

nic.active(True)

nic.ifconfig((NET_IP, NET_SN, NET_GW, NET_DNS))

ip, subnet, gateway, dns = nic.ifconfig()
print("IP address   :", ip)
print("Subnet mask  :", subnet)
print("Gateway      :", gateway)
print("DNS          :", dns)
print("MAC address  :", ':'.join(['%02x' % b for b in nic.config('mac')]))

s=socket.socket()
# Set timeout if needed (e.g., 30 seconds)
try:
    print("Connecting to {}:{}".format(DEST_IP, DEST_PORT))
    s.connect((DEST_IP, DEST_PORT))
    print("Loopback client Connect!")
    while True:
        data = s.recv(2048)
        if not data:
            # Server closed the connection
            raise OSError(errno.ECONNRESET, "server closed")
        print(data.decode("utf-8", "ignore"))
        if data != b"NULL":
            s.send(data)
except OSError as e:
    print("Client error:", e)
    raise
finally:
    s.close()

