import logging
import adafruit_ahtx0

from adafruit_extended_bus import ExtendedI2C
from ..schemas import Sensor, Attribute

# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-15s %(message)s')
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------

class AHT10(Sensor):

    def __init__(self):
        super().__init__()
        self._device = adafruit_ahtx0.AHTx0(ExtendedI2C(4))
        self._attributes = [
            Attribute("h", "humidity", "Float"),
            Attribute("t", "temperature", "Float")
        ]


    def raw_read(self):
        # Load default values in case of error
        hum = 0
        temp = 0

        try: # Try to read the i2c device
            hum = round(self._device.relative_humidity, 5)
            temp = round(self._device.temperature, 5)
        except Exception as e:
            logger.info("Error while reading the AHT10 sensor. Returning default values.")
            logger.error(str(e))

        return hum, temp
        