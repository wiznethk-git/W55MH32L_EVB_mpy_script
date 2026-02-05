from machine import UART
import time

uart = UART(2, 115200)
for i in range(10):
    uart.write(b"abc")
    time.sleep(0.1)

print("Waiting for USB-TTL input...")
time.sleep(5)
data = uart.readline()
print(data)

print ("Done")
