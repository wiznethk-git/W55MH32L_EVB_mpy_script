# photosensor_test.py
from machine import Pin, ADC
import time

# --- Configuration ---
SENSOR_PIN = "PA0"

# Initialize ADC
adc = ADC(Pin(SENSOR_PIN))

print("Photosensitive sensor test started")
print("Press Ctrl+C to stop\n")

while True:
    # Read raw ADC value
    value = adc.read_u16() 
    
    # Calculate percentage (0-100%)
    percentage = (value / 65535) * 100
    
    print("Raw: {:4d} | {:.1f}%".format(value, percentage))
    
    time.sleep(0.5)