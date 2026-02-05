from machine import RTC
import time

rtc = RTC()

# Set date/time   (example: 2026-Jan-23  Friday 15:42:00)
# weekday = 4 → Friday
rtc.datetime((2026, 1, 23, 4, 15, 42, 0, 0))

# Give RTC a moment to update
time.sleep_ms(100)

while True:
    t = rtc.datetime()
    print("{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}  weekday={}"
          .format(t[0], t[1], t[2], t[4], t[5], t[6], t[3]))
    time.sleep(3)