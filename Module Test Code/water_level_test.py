# water_level_test.py 
from machine import Pin, ADC
import time

# Choose an ADC-capable pin (try PA0, PA1, PB0, etc. if one doesn't work)
SENSOR_PIN = "PA0"

# Initialize ADC
adc = ADC(Pin(SENSOR_PIN))

print("Water level sensor test started")
print("Press Ctrl+C to stop\n")

while True:
    raw = adc.read_u16()
    max_val = 65535

    percent = (raw / max_val) * 100
    print(f"Raw: {raw:5d} | {percent:6.2f}%")
    time.sleep(0.5)