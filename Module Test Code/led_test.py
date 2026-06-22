# led_test.py
from machine import Pin
import time

led = Pin("PG8", Pin.OUT)

print("LED blinking on PG8...")
while True:
    led.on()
    print("LED ON")
    time.sleep(1)
    led.off()
    print("LED OFF")
    time.sleep(1)