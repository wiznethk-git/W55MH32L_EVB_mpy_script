# flame_sensor_test.py – Test flame sensor (Analog + Digital outputs)
from machine import Pin, ADC
import time

# --- Pin definitions (change to your actual wiring) ---
# Digital output (D) – connect to sensor's 'D' pin
do_pin = Pin("PG8", Pin.IN)

# Analog output (A) – connect to sensor's 'A' pin
adc = ADC(Pin("PA0"))

print("Flame Sensor Test")
print("=================")

while True:
    # 1. Read analog value (12-bit, 0-4095; higher value = less flame)
    adc_value = adc.read_u16() >> 4   # convert to 12-bit range
    
    # 2. Read digital value (0 = flame detected, 1 = no flame)
    do_state = do_pin.value()
    
    # 3. Print results
    print(f"AO Value: {adc_value:4d} | DO Pin: {do_state}")
    
    # 4. Simple alarm when digital output goes low
    if do_state == 0:
        print("*** FIRE DETECTED! ***")
    
    time.sleep(0.5)