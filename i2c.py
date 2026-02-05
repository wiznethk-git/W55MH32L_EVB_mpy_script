# aht20_simple_test.py

from machine import Pin, I2C
import utime
import ahtx0           # <-- the library file for ahtx0

# ───────────────────────────────────────
# Adjust these pins to match your wiring
# Most common choices:

# W55MH32L-EVB
i2c = I2C(1)     # PB7=SDA, PB6=SCL

# Create sensor object
sensor = ahtx0.AHT20(i2c)     # or AHT10(i2c) if you have the older model

print("AHT20 sensor test started\n")

while True:
    try:
        temp = sensor.temperature
        humi = sensor.relative_humidity
        
        print(f"Temperature : {temp:5.1f} °C")
        print(f"  Humidity  : {humi:5.1f} %rH")
        print("─" * 28)
        
    except OSError as e:
        print("Sensor read error:", e)
    
    utime.sleep_ms(2500)   # read ~every 2.5 seconds