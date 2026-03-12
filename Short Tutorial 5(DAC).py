from machine import DAC
import time

# Setup DAC on pin PA4 with 12-bit resolution
dac = DAC('PA4', bits=12)

print("DAC Output Test - Watch the multimeter!")
print("Connect multimeter between PA4 and GND")
print("Using 12-bit resolution (0-4095)")

voltages = [0, 0.825, 1.65, 2.475, 3.3]
names = ["0V", "0.825V", "1.65V", "2.475V", "3.3V"]

while True:
    for i in range(len(voltages)):
        # Convert voltage to 12-bit DAC value
        value = int((voltages[i] / 3.3) * 4095)
        dac.write(value)
        
        print(f"Output: {names[i]} (DAC value: {value})")
        time.sleep(1)
        
        