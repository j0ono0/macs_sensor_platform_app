import time
import json
import binascii
import ntptime
import machine

# To install: mpremote mip install umqtt.robust
from umqtt.robust import MQTTClient

import wifi_tools as wt
import sensors
import config as cfg

PIN_LED_RED = 5  # Red led
PIN_LED2_GREEN = 6  # Green led
PIN_BTN = 9  # Push button

# Timeout mqtt connect attempt
MQTT_TIMEOUT = 30

led_red = machine.Pin(PIN_LED_RED, machine.Pin.OUT)
led_green = machine.Pin(PIN_LED2_GREEN, machine.Pin.OUT)

# Ensure LEDs are off (sometimes left on when tinker via mpremote)
led_red.off()
led_green.off()

# value of 0 = button down
btn = machine.Pin(PIN_BTN, machine.Pin.IN)


def blink_led(led, cycles, duration_ms):
    for i in range(cycles):
        led.on()
        time.sleep_ms(duration_ms)
        led.off()
        time.sleep_ms(100)


def set_time():
    # Set time on device
    # TODO: cater for timeouts?
    for addr in cfg.NTP_SERVERS:
        try:
            ntptime.host = addr
            ntptime.settime()
            rtc = machine.RTC()
            print("time set from network:", rtc.datetime())
            return True
        except OSError:
            pass
    print("No NTP server found.")
    return False


def poll_sensor():
    temperature, humidity, battery = sensors.poll_all()
    YYYY, MM, DD, wd, hh, mm, ss, ffffff = [
        "%02d" % x for x in machine.RTC().datetime()
    ]
    msg = {
        "uid": "".join(["{:02x}".format(b) for b in machine.unique_id()]),
        "datetime": f"{YYYY}-{MM}-{DD}T{hh}:{mm}:{ss}+00:00",  # Sending UTC time
        "temperature": temperature,
        "humidity": humidity,
        "battery": battery,
    }
    return msg


def pub_mqtt_log(filename, topic, broker):
    c = MQTTClient(topic, broker)
    try:
        c.connect(timeout=MQTT_TIMEOUT)
    except Exception as e:
        # Connection to broker failed
        print(e)
        return False
    # Send all messages over a single connection
    with open(filename, "r") as f:
        for msg in f:
            c.publish(topic, msg, qos=0)

    c.disconnect()
    return True


def log_locally(filename, data):
    with open(filename, "a") as f:
        f.write(json.dumps(data))
        f.write("\n")


def start_polling():

    # TODO: investigate using machine.schedule. Timers callback should be minimal function only(!)
    # TODO: investigate asyncio for scheduling

    log_count = 0

    while True:

        data = poll_sensor()
        print(data)
        log_locally(cfg.TELEMETRY_LOG_FILE, data)
        log_count += 1
        # Show sign of life!
        blink_led(led_green, 2, 100)

        if log_count >= cfg.LOG_FULL:
            # Send local data to remote
            wlan = wt.connect()
            if wlan:
                led_red.on()
                if pub_mqtt_log(
                    cfg.TELEMETRY_LOG_FILE,
                    cfg.MQTT_TOPIC_TELEMETRY,
                    cfg.target_network["mqtt_addr"],
                ):
                    open(cfg.TELEMETRY_LOG_FILE, "w").close()
                    led_red.off()
                    # Network must be inactive for lightsleep to work correctly
                    wlan.active(False)
                else:
                    print("error connecting")
                    blink_led(led_red, 5, 500)

            # Reset cache threshold. Accumulate more data locally
            log_count = 0

        # dev testing: time.sleep !!! machine.lightsleep crashes REPL ############
        # time.sleep_ms(2000)
        ##########################################################################
        machine.lightsleep(cfg.READ_PERIOD * 1000)


##################################################################################

blink_led(led_green, 2, 100)

wlan = wt.connect()

if wlan:
    wlan.config(reconnects=5)
    # Set time on device successfully before commencing monitoring
    if set_time():
        wlan.active(False)
        blink_led(led_green, 2, 100)
        start_polling()


led_red.on()
raise OSError("Error connecting to network.")
