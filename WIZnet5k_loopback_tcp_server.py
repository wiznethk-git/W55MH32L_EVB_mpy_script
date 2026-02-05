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
ip_addr = nic.ifconfig()[0]
s.bind((ip_addr, LOCAL_PORT))
s.listen(5)
print("TEST server on {}:{}".format(ip_addr, LOCAL_PORT))

try:
    conn, addr = s.accept()
    print("Connected:", addr)
    print("Loopback server Open!")
# Set timeout if needed (e.g., 30 seconds)
# conn.settimeout(30)
    while True:
        data = conn.recv(2048)
        if not data:
            # Peer closed the socket gracefully
            raise OSError(errno.ECONNRESET, "peer closed")
        print(data.decode("utf-8", "ignore"))
        if data != b"NULL":
            conn.send(data)

except OSError as e:
    # Log and exit on fatal network error
    print("Server error:", e)
    raise
finally:
    try:
        conn.close()
    except Exception:
        pass
    s.close()
