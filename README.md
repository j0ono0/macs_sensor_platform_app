# macs_sensor_platform_app
Application code for macs sensor platform


# Install required 3rd party modules: 
```bash
mpremote mip install umqtt.robust
mpremote mip install github:jposada202020/MicroPython_SHT4X
```

## Testing mqtt communications
mqtt can be tested locally using Apache Mosquitto
- install Apache Mosquitto along with helper pub and sub apps
In three separate terminal windows run the following:
- Mosquitto broker
- Mosquitto subscriber
- Mosquitto publisher
Note: the network address must be of the computer running the mosquitto broker

```bash
# terminal 1
mosquitto

# terminal 2
mosquitto_sub -h '192.168.0.110' -t macs/telemetry

#terminal 3
mosquitto_pub -h '192.168.0.110' -t macs/telemetry -m 'hello macs?'
```

"Hello macs?" should arrive in the subscriber terminal.
edit config.py to the correct mqtt_addr and restart mocropython on the hardware. Telemetry data should now arrive to the mosquitto broker and appear in the subscriber terminal.