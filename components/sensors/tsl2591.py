import logging
import adafruit_tsl2591
import time
import settings

from adafruit_extended_bus import ExtendedI2C
from ..schemas import Sensor, Attribute

# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-15s %(message)s')
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------

class TSL2591(Sensor):

    def __init__(self):
        super().__init__()
        self._device = adafruit_tsl2591.TSL2591(ExtendedI2C(1))
        self._device.integration_time = adafruit_tsl2591.INTEGRATIONTIME_600MS
        self._device.gain = adafruit_tsl2591.GAIN_MAX
        self._attributes = [
            Attribute("f", "full", "String"),
            Attribute("i", "infrared", "String"),
            Attribute("l", "lux", "String"),
            Attribute("g", "gain", "Integer"),
            Attribute("it", "integration", "Integer"),
            Attribute("v", "version", "Float")
        ]


    def raw_read(self):

        # Load default values in case of error
        full = ""
        ir = ""
        lux = ""
        gain = self._device.gain
        integration = self._device.integration_time
        version = settings.get("DEVICE", "device.version", 0.0)

        self._device.enable()

        # Get current integration time. Its very important to wait the same 
        # amount of ms as the current integration time after enabling the 
        # device; otherwise it will not work properly
        if self._device.integration_time == adafruit_tsl2591.INTEGRATIONTIME_100MS:
            time.sleep(0.1)
        elif self._device.integration_time == adafruit_tsl2591.INTEGRATIONTIME_200MS:
            time.sleep(0.2)
        elif self._device.integration_time == adafruit_tsl2591.INTEGRATIONTIME_300MS:
            time.sleep(0.3)
        elif self._device.integration_time == adafruit_tsl2591.INTEGRATIONTIME_400MS:
            time.sleep(0.4)
        elif self._device.integration_time == adafruit_tsl2591.INTEGRATIONTIME_500MS:
            time.sleep(0.5)
        else:
            time.sleep(0.6)

        oversample = int(settings.get("DEVICE", "device.oversample", 6))
        for _ in range(oversample):
            temp_full = 0
            temp_ir = 0
            temp_lux = 0.0

            try: # Try to read the i2c device
                temp_full = self._device.full_spectrum
                temp_ir = self._device.infrared
                temp_lux = round(self._device.lux, 5)

            except Exception as e:
                logger.info("Error while reading the TSL2591 sensor. Returning default values.")
                logger.error(str(e))

            full += str(temp_full) + ","
            ir += str(temp_ir) + ","
            lux += str(temp_lux) + ","
            time.sleep(1)

        self._device.disable()
        return full[:-1], ir[:-1], lux[:-1], gain, integration, version
        
    
    def set_gain_level(self, gain_level):
        self._device.gain = gain_level

    
    def set_integration_level(self, integration_level):
        self._device.integration_time = integration_level
