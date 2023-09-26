import logging
import settings
import crud
import time
import utils
import os

import adafruit_tsl2591

from datetime import datetime, timezone
from threading import Thread
from hw_manager import HardwareManager
from paho.mqtt.client import Client

# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-15s %(message)s')
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------

def _server_handshake(device_id: str, type: str, timezone: str, attributes: list, static: list=None, lazy: list=None, commands: list=None):
    try:
        logger.info(f"Requesting for device {type}:{device_id}")
        if crud.get_device_by_id(device_id, type):
            logger.info(f"Device {type}:{device_id} found. Updating data...")
            crud.update_device(device_id, type, timezone, attributes, static=static, lazy=lazy, commands=commands)

        else:
            logger.info(f"Cannot found device {type}:{device_id}. Creating a new one...")
            crud.create_device(device_id, type, timezone, attributes, static=static, lazy=lazy, commands=commands)

    except Exception as e:
        logger.info("Error occurred while connecting to the server")
        logger.error(str(e))
        return False

    return True


def _create_log_file(device_id: str, type: str, current_time: datetime, attributes: list):
    attr_headers = "datetime "
    for attr in attributes: 
        attr_headers += f"; {attr['name']} "

    logging_file = settings.LOG_FILES_PATH + f"/{current_time.strftime(settings.LOG_NAME_FORMAT)}{type.lower()}.dat"
    with open(logging_file, 'w+') as file:
        file.write((
            f"# Data logged at (UTC): {current_time.strftime(settings.LOG_TIME_FORMAT)}\n"
            f"# \n"
            f"# Device: {device_id} ({type.lower()})\n"
            f"# {attr_headers} \n"
            f"# ----------------------------------------\n"
        ))
    return logging_file


def _log_data_into_file(logging_file: str, current_time: datetime, input_data: dict):
    logging_data = f"{current_time.strftime(settings.LOG_TIME_FORMAT)}"
    for value in input_data.values(): 
        logging_data += f";{value}"
    
    with open(logging_file, 'a+') as file:
        file.write(f"{logging_data}\n")


def _perform_readings(hw_manager, mqtt_client, freedsm_logging_file, sqm_logging_file):
    current_time = datetime.now(timezone.utc)
    sqm_readings = hw_manager.read_sqm()

    hw_manager.configure_light_sensor(gain=adafruit_tsl2591.GAIN_MAX)
    freedsm_readings_max = hw_manager.read_freedsm()

    try:
        _log_data_into_file(sqm_logging_file, current_time, sqm_readings)
    except IOError as e:
        logger.info("Cannot log SQM data...")
        logger.error(str(e))

    try:
        _log_data_into_file(freedsm_logging_file, current_time, freedsm_readings_max)
    except IOError as e:
        logger.info("Cannot log FreeDsm data...")
        logger.error(str(e))
    
    # Parse data to UltraLight V2 format
    sqm_readings = utils.json2ultralight(sqm_readings)
    freedsm_readings_max = utils.json2ultralight(freedsm_readings_max)

    # Send data to mqtt
    mqtt_client.publish(f"/sqm/{hw_manager.device_id}/attrs", sqm_readings)
    mqtt_client.publish(f"/freedsm/{hw_manager.device_id}/attrs", freedsm_readings_max)
    

def _error_loop(info: list, waiting_msg: str):
    print("Cannot init device:")
    [print(msg) for msg in info]
    print(waiting_msg)
    while True: pass
    # In the future, this while loop will be used to keep the app alive,
    # listening to the bluetooth enable button or to send msgs to the screen.

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    hw_manager = HardwareManager()

    logger.info("Starting hardware scan...")
    can_init, info = hw_manager.scan()
    logger.info("Hardware scan finished")

    if not can_init:
        waiting_msg = "Try to connect the missing piece(s) and restart the device."
        _error_loop(info, waiting_msg)

    # Checks if there is pending data from a previous session
    # WIP ...

    # Get current device data
    device_id = hw_manager.device_id
    device_tz = hw_manager.device_tz
    freedsm_attrs = hw_manager.freedsm_attrs
    sqm_attrs = hw_manager.sqm_attrs

    # Get which attrs have to be locally logged
    freedsm_logged_attrs = hw_manager.get_freedsm_logging_headers()
    sqm_logged_attrs = hw_manager.get_sqm_logging_headers()

    # Read GPS and Gyroscope on start
    one_shot_readings = hw_manager.read_one_shot_sensors()

    # Inclinometer control
    inclination = one_shot_readings.get("inc")
    if inclination:
        info = []
        angle_x = inclination.get("angleX")
        angle_y = inclination.get("angleY")

        if angle_x >= 10 or angle_x < -10: 
            info.append("Angle X too inclined")

        if angle_y >= 10 or angle_y < -10: 
            info.append("Angle Y too inclined")
        
        if info:
            waiting_msg = "Put the device on a flat surface and restart it"
            _error_loop(info, waiting_msg)

    # Initial communication with the server
    freedsm_online = _server_handshake(device_id, "FreeDsm", device_tz, freedsm_attrs)
    sqm_online = _server_handshake(device_id, "SQM", device_tz, sqm_attrs)

    # Activate offline mode if there is no connection with the server
    # WIP ...

    # Init logging files for this session
    os.makedirs(settings.LOG_FILES_PATH, exist_ok=True)
    current_time = datetime.now(timezone.utc)
    freedsm_logging_file = _create_log_file(device_id, "FreeDsm", current_time, freedsm_logged_attrs)
    sqm_logging_file = _create_log_file(device_id, "SQM", current_time, sqm_logged_attrs)
    logger.info("Logging files created")

    # Start MQTT client on a background thread
    mqtt_client = Client()
    mqtt_client.connect(settings.MQTT_HOST, settings.MQTT_PORT)
    mqtt_client.loop_start()
    logger.info("MQTT client initiated")

    # Send 'one shot' readings to IoTA, if there is any
    if one_shot_readings:
        mqtt_client.publish(f"/freedsm/{device_id}/attrs", utils.json2ultralight(one_shot_readings))
        mqtt_client.publish(f"/sqm/{device_id}/attrs", utils.json2ultralight(one_shot_readings))

    # Set the reading frequency
    freq_in_min = settings.DEVICE_FREQ * 60
    logger.info(f"Reading frequency set to: {settings.DEVICE_FREQ} minute(s)")

    while True:
        time.sleep(freq_in_min)
        reader_thread = Thread(target=_perform_readings, args=(hw_manager, mqtt_client, freedsm_logging_file, sqm_logging_file))
        reader_thread.start()
