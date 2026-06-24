# Lamp
from machine import Pin, ADC, PWM
import time, gc

# ===== Pin definitions =====
# Photosensor (analog input)
LDR_PIN = "PB0"
ldr = ADC(Pin(LDR_PIN))

# RGB LED (PWM pins) – produces white light
RED_PIN   = PWM(Pin("PA6", Pin.OUT))
GREEN_PIN = PWM(Pin("PB9", Pin.OUT))
BLUE_PIN  = PWM(Pin("PA0", Pin.OUT))

# Set PWM frequency
RED_PIN.freq(1000)
GREEN_PIN.freq(1000)
BLUE_PIN.freq(1000)

# ===== Configuration =====
# Adjust these values based on your environment
DARK_THRESHOLD = 200     # Below this, LED starts turning on (0-4095)
MAX_BRIGHTNESS = 255     # Maximum PWM duty (0-255)

# White color balance (adjust if white looks tinted)
# Higher values = more of that color
WHITE_BALANCE = (255, 255, 255)   # (R, G, B) – tweak to get pure white

# ===== Helper functions =====
def set_white(brightness):
    """
    Set white light with given brightness (0-255).
    Brightness is applied to all three channels with white balance.
    """
    r = int(WHITE_BALANCE[0] * brightness / MAX_BRIGHTNESS)
    g = int(WHITE_BALANCE[1] * brightness / MAX_BRIGHTNESS)
    b = int(WHITE_BALANCE[2] * brightness / MAX_BRIGHTNESS)
    
    RED_PIN.duty(r)
    GREEN_PIN.duty(g)
    BLUE_PIN.duty(b)

def map_value(value, in_min, in_max, out_min, out_max):
    """Map a value from one range to another."""
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# ===== Main loop =====
print("Adaptive White Light Controller")
print(f"Dark threshold: {DARK_THRESHOLD}")
print("Darker → brighter | Lighter → dimmer")
print("Press Ctrl+C to stop\n")

while True:
    # Read light level (0-4095)
    light_level = ldr.read_u16() >> 4   # convert to 12-bit (0-4095)
    
    # Calculate brightness based on darkness
    if light_level >= DARK_THRESHOLD:
        # Bright enough → LED off
        brightness = 0
        status = "BRIGHT → OFF"
    else:
        # Too dark → calculate brightness
        # Darker = lower light_level = higher brightness
        brightness = map_value(light_level, 0, DARK_THRESHOLD, MAX_BRIGHTNESS, 0)
        brightness = max(0, min(MAX_BRIGHTNESS, brightness))
        status = f"DARK → brightness: {brightness:3d}%"
    
    # Apply brightness to white light
    set_white(brightness)
    
    # Show status (only when changed)
    print(f"Light: {light_level:4d} | {status}")
    time.sleep(0.3)
    gc.collect()