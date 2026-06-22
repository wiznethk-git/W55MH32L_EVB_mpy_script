# motor_test.py
from machine import Pin
import time

# Change pin names to your actual wiring
INA = Pin("PG8", Pin.OUT)
INB = Pin("PG7", Pin.OUT)

def motor_forward():
    print("move forward")
    INA.value(1)
    INB.value(0)

def motor_backward():
    print("move backward")
    INA.value(0)
    INB.value(1)

def motor_stop():
    print("stop")
    INA.value(0)
    INB.value(0)

def motor_brake():
    INA.value(1)
    INB.value(1)

# Demo: forward 2s, stop 1s, reverse 2s, stop
motor_forward()
time.sleep(2)
motor_stop()
time.sleep(3)
motor_backward()
time.sleep(2)
motor_stop()