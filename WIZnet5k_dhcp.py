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


try: nic.ifconfig("dhcp")
except Exception: pass

if nic.isconnected():
    print("\nConnected!")
    config = nic.ifconfig()
    print("IP address:   ", config[0])
    print("Subnet mask:  ", config[1])
    print("Gateway:      ", config[2])
    print("DNS:          ", config[3])
    print("MAC address  :", ':'.join(['%02x' % b for b in nic.config('mac')]))
