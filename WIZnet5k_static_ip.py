import network
import time
from machine import SPI, Pin

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