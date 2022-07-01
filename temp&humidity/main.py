from mqtt import MQTTClient
import time
import ujson
import machine
from machine import Pin, SoftI2C
from time import sleep
from dht import DHT11
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from config import SERIAL_NUMBER, MQTT_BROKER, TOKEN

# Setup
sensor = DHT11(Pin(14))
I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

def sub_cb(topic, msg):
   print(msg)

# MQTT Setup
client = MQTTClient(SERIAL_NUMBER,
                    MQTT_BROKER,
                    user=TOKEN,
                    password=TOKEN,
                    port=1883)

client.set_callback(sub_cb)
client.connect()
print('connected')

my_topic = 'dtck-pub/project-1/fed60c70-6232-4997-969a-3f3589be09e4/TEMPERATURE'
my_topic2 = 'dtck-pub/project-1/fed60c70-6232-4997-969a-3f3589be09e4/HUMIDITY'

payload = 0
payload2 = 0


while True:
    lcd.clear()
    sensor.measure()
    temp = sensor.temperature()
    humidity = sensor.humidity()

    print(lcd.putstr('Temp: %2.0f C' %temp + '\n'))
    print(lcd.putstr('Humidity: %2.0f%%' %humidity))


    payload = temp
    payload2 = humidity
    client.publish(topic=my_topic, msg=str(payload))
    client.publish(topic=my_topic2, msg=str(payload2))


    client.check_msg()
    time.sleep(120)
