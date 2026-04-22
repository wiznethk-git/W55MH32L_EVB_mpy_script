from machine import SDCard
import os

sd = SDCard()

# Card hardware info
info = sd.info()
print("SD CARD HARDWARE INFO")
print("-" * 30)
print(f"Total capacity: {info[0]:,} bytes")
print(f"Total capacity: {info[0] / (1024**3):.2f} GB")
print(f"Block size: {info[1]} bytes")
print(f"Card type/status: {info[2]}")
print(f"Total blocks: {info[0] // info[1]:,}")


# Write
with open("/sd/myfile.txt", "w") as f:
    f.write("Line 1\nLine 2\nLine 3\n")
print("✓ File written: /sd/myfile.txt")

# Read
with open("/sd/myfile.txt", "r") as f:
    print("\nFile content:")
    print(f.read())


