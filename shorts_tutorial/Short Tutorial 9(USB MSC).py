import machine

# Set to Mass Storage mode 
machine.usb_mode('MSC')
print("Board in MSC mode")

print("=" * 40)
print("MSC MODE DEMO - Mass Storage")
print("=" * 40)

# Create a file on the flash drive
with open('/flash/data.txt', 'w') as f:
    f.write("This file is on the USB drive!\n")
    
with open('/flash/data.txt', 'r') as f:
    print(f.read())

print("File 'data.txt' created on USB drive")
