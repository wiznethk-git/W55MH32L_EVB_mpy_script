# adc.py
# Read potentiometer on W55MH32L-EVB (MicroPython)

from machine import ADC, Pin
from time import sleep

# Create ADC object on PA4(ADC channel 0)
pot = ADC(Pin("PA4"))          # or ADC(0) — both work

print("Potentiometer ADC test started\n")

while True:
    raw = pot.read_u16()              # 0 .. 65535 (16-bit, even though ADC is 12-bit)
    voltage = (raw / 65535) * 3.3     # convert to volts (assuming 3.3 V reference)
    percent = (raw / 65535) * 100     # percentage 0–100%

    print(f"Raw: {raw:5d}   Voltage: {voltage:4.2f} V   {percent:5.1f} %")
    
    sleep(0.5)   # update every 0.5 seconds