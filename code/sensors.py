# NOTE: this requires installation of:
# https://github.com/jposada202020/MicroPython_SHT4X/tree/master

# Install with command"
# mpremote mip install github:jposada202020/MicroPython_SHT4X


import time
from machine import Pin, I2C, ADC
from micropython_sht4x import sht4x

# Battery
ENABLE_BATT = 10
READ_BATT = 4
READ_COUNT = 60
en_batt = Pin(ENABLE_BATT, Pin.OUT)
batt = ADC(Pin(READ_BATT))
batt.atten(ADC.ATTN_2_5DB)

# Humidity and Temperature sensor
SDA_PIN = 21
SCL_PIN = 20
SAMPLE_SIZE = 10

i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN))  # Correct I2C pins for RP2040
sht = sht4x.SHT4X(i2c)


def read_battery():
    en_batt.on()
    time.sleep_ms(5)
    uv = batt.read_uv()
    en_batt.off()
    return uv


def poll_all():
    battery = ((read_battery() / 1000000) * (28 + 10)) / 10
    temperature, rel_humidity = sht.measurements
    return (temperature, rel_humidity, battery)
