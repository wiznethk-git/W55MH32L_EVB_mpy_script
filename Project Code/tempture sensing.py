# main.py – DHT22 temperature monitor with motor + LED control
from machine import Pin, I2C
import time, gc
from dht import DHT22
from tm1650 import TM1650

# ===== Pin definitions =====
DHT_PIN = "PC6"

# Motor (L9110S: INA, INB)
MOTOR_INA = Pin("PG8", Pin.OUT)
MOTOR_INB = Pin("PG7", Pin.OUT)

# LED
LED_PIN = Pin("PC7", Pin.OUT)

# TM1650 display (CLK = PB10, DIO = PB11)
i2c = I2C(1)
display = TM1650(i2c)

# ===== Helper functions =====
def motor_on():
    MOTOR_INA.value(1)
    MOTOR_INB.value(0)
    print("Motor: ON")

def motor_off():
    MOTOR_INA.value(0)
    MOTOR_INB.value(0)
    print("Motor: OFF")

def led_on():
    LED_PIN.value(1)
    print("LED: ON")

def led_off():
    LED_PIN.value(0)
    print("LED: OFF")

def display_temp(temp):
    # Convert to integer with 1 decimal place (23.6 -> 236)
    val = int(round(temp * 10, 0))

    # Extract digits (4 digits: thousands, hundreds, tens, ones)
    d0 = val // 1000
    d1 = (val // 100) % 10
    d2 = (val // 10) % 10
    d3 = val % 10
    
    display.write_digit(1, d1, dp=False)   
    display.write_digit(2, d2, dp=True)
    display.write_digit(3, d3, dp=False)


# ===== Initialise sensor =====
sensor = DHT22(DHT_PIN)
display.set_brightness(5)

print("DHT22 Temperature Monitor")
print("Threshold: >25°C → Motor + LED ON")
print("Press Ctrl+C to stop\n")

# ===== Main loop =====
while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        # Display temperature with decimal point
        display_temp(temp)

        print(f"Temp: {temp:.1f}°C  Hum: {hum:.1f}%")

        # Control motor and LED based on temperature
        if temp >= 23.0:
            motor_on()
            led_on()
        else:
            motor_off()
            led_off()

    except Exception as e:
        print("Sensor error:", e)

    time.sleep(2)
    gc.collect()