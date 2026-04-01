import machine
import time

uart = machine.UART(2, 115200)

print("Initializing SFA30...")

# Reset sensor
uart.write(bytearray([0x7E, 0x00, 0xD3, 0x00, 0x2C, 0x7E]))
time.sleep(5)

# Configure sensor
uart.write(bytearray([0x7E, 0x00, 0x00, 0x01, 0x00, 0xFE, 0x7E]))
time.sleep(2)
uart.read()  # Clear buffer

print("Reading temperature...")

while True:
    # Request reading
    uart.write(bytearray([0x7E, 0x00, 0x03, 0x01, 0x02, 0xF9, 0x7E]))
    time.sleep(0.2)
    
    # Read response
    data = uart.read()
    
    if data and len(data) >= 9 and data[0] == 0x7E and data[-1] == 0x7E:
        # Extract temperature (bytes 7 and 8)
        temp_raw = (data[7] << 8) | data[8]
        temp = temp_raw / 200.0 - 5.0
        print(f"{temp:.1f}°C")
    else:
        print("No data")
    
    time.sleep(2)
    
    