import json
import machine
from machine import Pin

PIN_LED_RED = 5 # Red led
PIN_LED2_GREEN = 6 # Green led
PIN_BTN = 9 # Push button


led_red = Pin(PIN_LED_RED, Pin.OUT)
led_green = Pin(PIN_LED2_GREEN, Pin.OUT)

# value of 0 = button down
btn = Pin(PIN_BTN, Pin.IN) 




def log_telemetry_locally(data):
    with open("sht4x.log","a") as f:
        f.write(json.dumps(data))


# Function for interrupt management 
def ISR_led_indicator(pin):
    led_red.toggle()


# btn.irq(handler=ISR_led_indicator, trigger=Pin.IRQ_FALLING, wake=machine.DEEPSLEEP|machine.SLEEP)

def test():
    for i in range(6):
        led_red.toggle()
        machine.lightsleep(5000)
    led_green.toggle()

