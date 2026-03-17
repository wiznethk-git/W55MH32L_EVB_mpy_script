from machine import Pin, ADC
import time

# Setup ADC on pin PA0
adc = ADC(Pin("PA0"))

print("ADC Slider Demo")
print("Move the slider to see values change")


while True:
    # Read raw ADC value (0-65535 for 16-bit)
    raw_value = 65535 - adc.read_u16()
    
    # Convert to voltage (0-3.3V)
    voltage = (raw_value / 65535) * 3.3 
    
    # Convert to percentage (0-100%)
    percentage = int((raw_value / 65535) * 100)
    
    # Print all values
    print(f"Raw: {raw_value:5d} | Voltage: {voltage:.2f}V | {percentage:3d}%")
    
    # Visual bar
    bar = "█" * (percentage // 5)
    print(f"[{bar:<20}]")
    print()
    
    time.sleep(0.1)


