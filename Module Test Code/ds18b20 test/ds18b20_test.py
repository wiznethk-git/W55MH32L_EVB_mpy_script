# ds18b20_test.py
from machine import Pin
import onewire, ds18x20
import time

# === Wiring ===
# DS18B20 Pin   -> W55MH32L-EVB
#   VDD (red)   -> 3.3V
#   DQ  (yellow)-> GPIO (e.g., PG6)
#   GND (black) -> GND
# Add a 4.7kΩ pull-up resistor between DQ and 3.3V.

# === Pin setup ===
DQ_PIN = "PG4"          # change to your data pin
ow = onewire.OneWire(Pin(DQ_PIN))
ds = ds18x20.DS18X20(ow)

# === Scan for devices ===
roms = ds.scan()
print("Found DS18B20 devices:", roms)
if not roms:
    print("No DS18B20 found. Check wiring and pull-up resistor.")
    raise SystemExit

print("Starting temperature reading...\n")

# === Main loop ===
while True:
    # 1. Start temperature conversion on all devices
    ds.convert_temp()
    # 2. Wait at least 750 ms for conversion (DS18B20 max conversion time)
    time.sleep_ms(750)
    # 3. Read and print temperature for each device
    for rom in roms:
        temp = ds.read_temp(rom)
        print(f"Device {''.join('{:02x}'.format(b) for b in rom)}: {temp:.2f} °C")
    print()
    time.sleep(1)   # read every 1 seconds (adjust as needed)