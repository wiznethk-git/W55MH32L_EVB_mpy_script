from machine import WDT
import time

# This is SAFE - feeds watchdog
print("Safe WDT - feeding every second")
wdt = WDT(timeout=3000)
for i in range(6):
    wdt.feed()  # Reset the timer
    print(f"Fed WDT at {i+1} seconds")
    time.sleep(1)
print("System stayed alive!")