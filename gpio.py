from machine import Pin
import time

button = Pin("PG6", Pin.IN)
led = Pin ("PD14", Pin.OUT)

while True:
    if button.value() == 0:
        led.value(0)
    else:
        led.value(1)