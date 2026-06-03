import network
import socket
import time
from machine import Pin, SPI

# Ethernet setup (adjust IP to your network)
spi = SPI(2, baudrate=8_000_000)
cs = Pin("PB12", Pin.OUT)
rst = Pin("PD9", Pin.OUT)

nic = network.WIZNET5K(spi, cs, rst)
nic.active(True)
nic.ifconfig(("10.0.1.50", "255.255.255.0", "10.0.1.254", "8.8.8.8"))
time.sleep(2)                       # let interface stabilise

domain = "docs.w5500.com"             # change to any domain
print(f"Resolving {domain} ...")
try:
    addr = socket.getaddrinfo(domain, 80)[0][-1][0]
    print(f"IP address of {domain}: {addr}")
except Exception as e:
    print(f"DNS failed: {e}")
    
    
    
    
    
    
    
    
    
    
    
    
    
    