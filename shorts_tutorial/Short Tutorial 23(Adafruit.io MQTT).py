import network
import time
from machine import Pin, SPI
from umqtt.simple import MQTTClient
from secrets import ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY

# ========== Ethernet setup ==========
spi = SPI(2, baudrate=8_000_000)
cs = Pin("PB12", Pin.OUT)
rst = Pin("PD9", Pin.OUT)

nic = network.WIZNET5K(spi, cs, rst)
nic.active(True)
nic.ifconfig('dhcp')
time.sleep(3)
print("Board IP:", nic.ifconfig()[0])

# ========== Adafruit IO settings ==========
CONTROL_FEED = "led"          # feed to subscribe (receive commands)
STATUS_FEED  = "status"       # feed to publish (send status)

MQTT_HOST = "io.adafruit.com"
MQTT_PORT = 1883
sub_topic = f"{ADAFRUIT_IO_USERNAME}/feeds/{CONTROL_FEED}"
pub_topic = f"{ADAFRUIT_IO_USERNAME}/feeds/{STATUS_FEED}"
client_id = f"pico-both-{ADAFRUIT_IO_USERNAME}"

# ========== MQTT callback ==========
def mqtt_callback(topic, msg):
    print(f"Received on {topic.decode()}: {msg.decode()}")
    if msg == b"ON":
        led.on()
        publish_status("LED turned ON")
    elif msg == b"OFF":
        led.off()
        publish_status("LED turned OFF")
    else:
        print("Unknown command")

def publish_status(message):
    try:
        client.publish(pub_topic, message)
        print(f"Published to {STATUS_FEED}: {message}")
    except Exception as e:
        print("Publish error:", e)


# ========== Connect and subscribe ==========
print(f"Connecting to MQTT broker...")
client = MQTTClient(client_id, MQTT_HOST, MQTT_PORT,
                    ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.set_callback(mqtt_callback)
client.connect()
print("Connected!")

client.subscribe(sub_topic)
print(f"Subscribed to: {sub_topic}")
print(f"Will publish status to: {pub_topic}")

# LED on PG8 (change to your pin)
led = Pin("PG8", Pin.OUT)
led.off()
publish_status("LED turned OFF")


# ========== Main loop ==========
print("Waiting for messages... (Ctrl+C to stop)\n")
try:
    while True:
        client.check_msg()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nDisconnecting...")
    client.disconnect()