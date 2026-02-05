from machine import Pin, DAC

# Create DAC on GPIO PA4
dac = DAC(Pin("PA4"))

# Set ~1.65 V (half scale)
dac.write(128)
print("DAC_output")

