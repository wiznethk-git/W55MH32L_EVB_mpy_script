from machine import Pin, PWM
import time


servo_pin = "PA0"

# Initialize PWM
servo = PWM(Pin(servo_pin))
servo.freq(50)  # 50Hz for standard servos (20ms period)

def set_angle(angle):
    """Set servo angle from 0 to 180 degrees"""
    duty = int(1638 + (angle / 180) * 6554)
    servo.duty_u16(duty)

print("Testing servo on GPIO", servo_pin)
print("Moving to 0°...")
set_angle(0)
time.sleep(1)

print("Moving to 90°...")
set_angle(90)
time.sleep(1)

print("Moving to 180°...")
set_angle(180)
time.sleep(1)

print("Sweeping back and forth...")
while True:
    for angle in range(0, 181, 10):
        set_angle(angle)
        time.sleep(0.05)
    for angle in range(180, -1, -10):
        set_angle(angle)
        time.sleep(0.05)