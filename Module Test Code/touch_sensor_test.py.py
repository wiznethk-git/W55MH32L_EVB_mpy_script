# touch_sensor.py
from machine import Pin
import time

TOUCH_PIN = "PG8"
touch = Pin(TOUCH_PIN, Pin.IN)

print("Touch test ready. Touch the sensor...")
last = False
while True:
    current = touch.value() == 1   # change to == 0 if active low
    if current and not last:
        print("Touch detected!")
        time.sleep_ms(200)   # debounce
    last = current
    time.sleep_ms(50)