# tm1650_testing.py
from tm1650 import TM1650
from machine import I2C
import time

# Create hardware I2C2 (bus 2) with the correct pins
i2c = I2C(2)

# Pass the I2C object to the display
disp = TM1650(i2c)
disp.set_brightness(5)
disp.show_number(1234)
print("Showing 1234")
time.sleep(2)
for n in range(1,6):
    disp.show_number(n * 1111)
    print("Showing",n * 1111)
    time.sleep(1)
print("Done")
disp.clear()