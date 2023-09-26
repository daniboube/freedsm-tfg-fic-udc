import os
import configparser as cf

# -----------------------------------------------------------------------------

# Build all paths on the project with ROOT_DIR + r"/another_path"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

config = cf.RawConfigParser()
config.read(ROOT_DIR + r"/config.properties")

# -----------------------------------------------------------------------------

def get(section, option, default_value):
    value = config.get(section, option, fallback=default_value)
    try:
        value_as_float = float(value)
        return value_as_float
    except ValueError:
        return value


def set(section, option, value):
    if config.has_option(section, option):
        config.set(section, option, value)
        with open(ROOT_DIR + r"/config.properties", 'w') as configfile:
            config.write(configfile)
    else:
        raise KeyError

# -----------------------------------------------------------------------------

# DEVICE
DEVICE_FREQ = int(get("DEVICE", "device.freq", 5))

# MQTT
MQTT_HOST = get("MQTT", "mqtt.host", "localhost")
MQTT_PORT = int(get("MQTT", "mqtt.port", 1883))

# IOT_AGENT
IOT_AGENT_HOST = get("IOT_AGENT", "iot_agent.host", "localhost")
IOT_AGENT_PORT = int(get("IOT_AGENT", "iot_agent.port", 4041))

# ORION_CONTEXT
ORION_HOST = get("ORION_CONTEXT", "orion.host", "localhost")
ORION_PORT = int(get("ORION_CONTEXT", "orion.port", 1026))

# LOGGING FILES
LOG_FILES_PATH = os.path.dirname(ROOT_DIR) + r"/freedsm-logs"
LOG_NAME_FORMAT = "%Y_%m_%d.%H_%M_%S."
LOG_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
