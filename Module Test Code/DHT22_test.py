# test_dht22.py
from dht import DHT22
import time

# Change to your actual data pin
SENSOR_PIN = "PG8"

sensor = DHT22(SENSOR_PIN)
print(f"DHT22 test on pin {SENSOR_PIN}")
print("Press Ctrl+C to stop\n")

while True:
    try:
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        print(f"Temp: {t:.1f}°C  Hum: {h:.1f}%")
    except Exception as e:
        print("Error:", e)
    time.sleep(2)