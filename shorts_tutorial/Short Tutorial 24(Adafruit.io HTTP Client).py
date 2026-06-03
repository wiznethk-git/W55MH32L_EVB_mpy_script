import network
import time
import ahtx0
import urequests
import ujson, gc
import machine
from machine import Pin, SPI, I2C
from secrets import ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY

# ========== AHT20 sensor (I2C) ==========
i2c = I2C(1)          # PB7=SDA, PB6=SCL
sensor = ahtx0.AHT20(i2c)

# ========== Ethernet setup ==========
spi = SPI(2, baudrate=8_000_000)
cs = Pin("PB12", Pin.OUT)
rst = Pin("PD9", Pin.OUT)

nic = network.WIZNET5K(spi, cs, rst)
nic.active(True)
nic.ifconfig('dhcp')          # use DHCP
time.sleep(3)
print("W55MH32L-EVB IP:", nic.ifconfig()[0])

# ========== Adafruit IO configuration ==========
FEED_TEMP = "temperature"
FEED_HUMI = "humidity"


# HTTP settings (plain HTTP – likely rejected by Adafruit IO)
HTTP_HOST = "io.adafruit.com"
HTTP_PORT = 80

HTTP_BASE = "http://" + HTTP_HOST + "/api/v2/" + ADAFRUIT_IO_USERNAME + "/feeds"
HTTP_HEADERS = {
    "X-AIO-Key": ADAFRUIT_IO_KEY,
    "Content-Type": "application/json"
}

def publish(temp, humi):
    try:
        url_temp = HTTP_BASE + "/" + FEED_TEMP + "/data"
        url_humi = HTTP_BASE + "/" + FEED_HUMI + "/data"
        payload_temp = ujson.dumps({"value": temp})
        payload_humi = ujson.dumps({"value": humi})
        # Note: plain HTTP (port 80) – may be rejected by Adafruit IO.
        r1 = urequests.post(url_temp, data=payload_temp, headers=HTTP_HEADERS)
        r2 = urequests.post(url_humi, data=payload_humi, headers=HTTP_HEADERS)
        print(f"HTTP temp status: {r1.status_code}, humi status: {r2.status_code}")
        r1.close()
        r2.close()
        return True
    except Exception as e:
        print("HTTP error:", e)
        return False

# ========== Main loop ==========

while True:
    try:
        temp = round(sensor.temperature, 1)
        humi = round(sensor.relative_humidity, 1)
        print(f"Sensor: {temp}°C, {humi}%")
        publish(temp, humi)
        gc.collect()
        time.sleep(3)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        machine.soft_reset()
        break

    
