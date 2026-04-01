# main.py - Example using USB VCP for communication
import machine
import time

machine.usb_mode('VCP')

# Get the VCP object (id=0 is the default/only one)
vcp = machine.USB_VCP()

print("VCP example started. Type characters in your terminal...")

while True:
    # Check if any data is available from host (PC)
    data = vcp.write("\r\nType characters in your terminal...")
    if vcp.any():
        data = vcp.read()                  # Read all available bytes
        if data:
            print("\n\rReceived from PC:", data)

    time.sleep(2)  # Every 2 seconds
    
    
    
    
    
    
    
    