READ_PERIOD = 60  # periods units: seconds
LOG_FULL = 5  # Attempt to send when log is 'full'

# Timeout mqtt connect attempt
MQTT_TIMEOUT = 20

TELEMETRY_LOG_FILE = "telemetry.log"

NTP_SERVERS = [
    "192.168.0.100",  # rpi4 on demo network
    "192.168.0.91",  # rpi4 on home network
    "pool.ntp.org",  # www
]

MQTT_TOPIC_TELEMETRY = "macs/telemetry"

known_networks = [
    {
        "ssid": "SensorNetworkDemo",
        "password": "demo04082025",
        "mqtt_addr": "192.168.0.100",
    },
    {
        "ssid": "TelstraCD4F4B",
        "password": "nd8na68rcj",
        "mqtt_addr": "192.168.0.91",
    },
]
TARGET_SSID = "TelstraCD4F4B"


# Converience function - return network dict matching TARGET_SSID
def __getattr__(name):
    if name == "target_network":
        return next((n for n in known_networks if n["ssid"] == TARGET_SSID), None)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
