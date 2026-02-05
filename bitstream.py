from machine import Pin, bitstream
import time

# Define the timing for the WS2812 based on datasheet specifics for 800kHz
# Format: (high_time_0, low_time_0, high_time_1, low_time_1) in nanoseconds
TIMING = [400, 850, 800, 450] 

# Set up the data pin for the LEDs. Adjust 'GPX' to your board's specific pin (eg. PD5)
LED_PIN = Pin("PD5", Pin.OUT, value=0) 
NUM_LEDS = 8 # Number of LEDs in your strip

def create_rgb_buffer(red, green, blue):
    """Creates a bytearray for a single RGB color."""
    return bytearray([red, green, blue])

def update_leds(buffer):
    """Transmits the buffer data to the NeoPixel strip using bitstream."""
    # Encoding 0 is "high low" pulse duration modulation
    bitstream(LED_PIN, 0, TIMING, buffer)

# Animation cycle example (fade in/out red)
print("Starting bitstream NeoPixel animation...")
while True:
    # Fade in
    for brightness in range(0, 256, 10):
        buf = bytearray()
        color = create_rgb_buffer(brightness, 0, 0)
        for _ in range(NUM_LEDS):
            buf.extend(color)
        update_leds(buf)
        time.sleep(0.05)
        
    # Fade out
    for brightness in range(255, -1, -10):
        buf = bytearray()
        color = create_rgb_buffer(brightness, 0, 0)
        for _ in range(NUM_LEDS):
            buf.extend(color)
        update_leds(buf)
        time.sleep(0.05)
