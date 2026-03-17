from machine import Pin
import time

# Button on PG3
button = Pin("PG3", Pin.IN)

# LED on PB6 (output)
led = Pin("PB6", Pin.OUT)

# Turn LED off initially
led.value(0)

while True:
    if button.value() == 1:  # Button pressed
        led.value(1)          # LED on
        print("Button Pressed - LED ON")
    else:                      # Button released
        led.value(0)          # LED off
        print("Button Released - LED OFF")
    
    time.sleep(0.1)  # Small delay to avoid button bounce
