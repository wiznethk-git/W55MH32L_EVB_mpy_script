import network
import ntptime
import tm1637
import time, gc
from machine import Pin, SPI, RTC

# ----- Ethernet setup (your working config) -----
spi = SPI(2, baudrate=8_000_000)
cs  = Pin("PB12", Pin.OUT)
rst = Pin("PD9", Pin.OUT)

nic = network.WIZNET5K(spi, cs, rst)
nic.active(True)
nic.ifconfig(("10.0.1.50", "255.255.255.0", "10.0.1.254", "8.8.8.8"))
time.sleep(2)

print("Board IP:", nic.ifconfig()[0])


# ----- Setup TM1637 display -----
CLK_PIN = "PG7"   # clock pin
DIO_PIN = "PG8"   # data pin
display = tm1637.TM1637(clk=Pin(CLK_PIN, Pin.OUT),
                        dio=Pin(DIO_PIN, Pin.OUT))
display.brightness(3)


# Set wrong time to 10:30 (2026-01-01 10:30:00)
rtc=RTC()
rtc.datetime((2026,1,1,6,10,30,0,0))  

# Show wrong time (10:30) for 5 seconds
for _ in range(25):
    t=rtc.datetime();
    display.numbers(t[4],t[5]);
    time.sleep(0.2)


# ----- Sync RTC once at start -----
ntptime.host = "162.159.200.1"   # pool.ntp.org IP
ntptime.timeout = 5
print("Syncing time...")
ntptime.settime()
print("Time synced.")

print("\nDisplaying time on 7‑segment and console. (Ctrl+C to stop)\n")
try:
    while True:
        t = rtc.datetime()
        hour   = t[4]
        minute = t[5]
        second = t[6]

        # Update 7‑segment display
        display.numbers(hour, minute)

        # Print to shell/console
        print("\r{:02d}:{:02d}:{:02d}".format(hour, minute, second), end="")
        
        gc.collect()

        time.sleep(0.5)   # refresh rate
except KeyboardInterrupt:
    print("\nDisplay stopped.")
    display.write([0, 0, 0, 0])