# passive_buzzer_test.py
from machine import Pin, PWM
import time

# --- Configuration ---
BUZZER_PIN = "PA0"
buzzer = PWM(Pin(BUZZER_PIN))


# Play a rising scale
print("Playing rising tones (200-2000 Hz)...")
for freq in range(200, 2001, 200):
    print("Current freq:", freq)
    buzzer.freq(freq)
    buzzer.duty_u16(32768)
    time.sleep(0.3)
    buzzer.duty_u16(0)
    time.sleep(0.1)

buzzer.deinit()
print("Done.")