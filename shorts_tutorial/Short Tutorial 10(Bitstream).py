from machine import Pin, bitstream
import time, gc

# Define the timing for the WS2812 based on datasheet specifics for 800kHz
# Format: (high_time_0, low_time_0, high_time_1, low_time_1) in nanoseconds
TIMING = [400, 850, 800, 450] 

# Set up the data pin for the LEDs
LED_PIN = Pin("PD5", Pin.OUT, value=0) 
NUM_LEDS = 12  # Number of LEDs in your strip

def update_leds(red, green, blue):
    """Sets all LEDs to the specified RGB color."""
    buffer = bytearray()
    for _ in range(NUM_LEDS):
        buffer.extend(bytearray([green, red, blue]))
    bitstream(LED_PIN, 0, TIMING, buffer)
    time.sleep(0.01)
    bitstream(LED_PIN, 0, TIMING, buffer)

print("Starting simple color cycling...")
while True:
    # Red
    print("Red")
    update_leds(30, 0, 0)
    time.sleep(1)
    
    # Green
    print("Green")
    update_leds(0, 30, 0)
    time.sleep(1)
    
    # Blue
    print("Blue")
    update_leds(0, 0, 30)
    time.sleep(1)
    
    gc.collect()
