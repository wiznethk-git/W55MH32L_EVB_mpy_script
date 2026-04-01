# main.py - Example using USB VCP for communication
from machine import USB_VCP
import time

# Get the VCP object (id=0 is the default/only one)
vcp = USB_VCP()

print("VCP example started. Type characters in your terminal...")

while True:
    # Check if any data is available from host (PC)
    if vcp.any():
        data = vcp.read()                  # Read all available bytes
        if data:
            print("Received from PC:", data)
            
            # Echo back what was received (with a prefix)
            vcp.write(b"Echo: ")
            vcp.write(data)
            vcp.write(b"\r\n")

    # Send periodic message to PC (visible in your terminal2
    time.sleep_ms(2000)  # Every 2 seconds