# W55MH32L-EVB — low-level SPI test (read VERSIONR = 0x04)
from machine import Pin, SPI
import time

spi = SPI(1, baudrate=5_000_000, polarity=0, phase=0)

cs  = Pin("PA4", Pin.OUT)
rst = Pin("PA3", Pin.OUT)


# Optional hardware reset
rst.value(0)
time.sleep_ms(10)
rst.value(1)
time.sleep_ms(200)

cs.value(1)   # deselect

def read_version():
    cmd = bytearray([0x00, 0x39, 0x00])   # addr 0x0039, control byte read common block
    rx  = bytearray(4)

    cs.value(0)
    spi.write(cmd)
    rx=spi.read(1)
    print(rx)
    cs.value(1)

    return rx[0]

print("SPI test...")

ver = read_version()
print(f"VERSIONR register = 0x{ver:02X}")

if ver == 0x04:
    print("→ SUCCESS: SPI connection is working! W5500 Chip detected.")
else:
    print("→ FAIL — check power, USB cable, or try slower baudrate (e.g. 1_000_000)")

