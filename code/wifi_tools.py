import json
import machine, network
import time

import config as cfg

# To install: mpremote mip install umqtt.robust
from umqtt.robust import MQTTClient


def connect():

    TIMEOUT_PERIOD = 30000  # 30secs

    wlan = network.WLAN()
    wlan.active(True)
    available_nets = {n[0].decode("utf-8"): n for n in wlan.scan()}
    target_network = cfg.target_network

    if target_network["ssid"] in available_nets.keys():
        print(f"Attempting connection to {target_network['ssid']}")

        next_timeout = time.ticks_add(time.ticks_ms(), TIMEOUT_PERIOD)

        wlan.connect(target_network["ssid"], target_network["password"])

        while not wlan.isconnected():
            machine.idle()

            if time.ticks_diff(next_timeout, time.ticks_ms()) < 0:
                print("Connection falied (timed out).")
                wlan.active(False)
                return None

        print("network config:", wlan.ipconfig("addr4"))
        return wlan


def connect_mqtt_client(topic, broker):
    c = MQTTClient(topic, broker)
    try:
        c.connect(timeout=cfg.MQTT_TIMEOUT)
        c.disconnect()
        return c
    except Exception as e:
        # Connection to broker failed
        print(e)
        return None
