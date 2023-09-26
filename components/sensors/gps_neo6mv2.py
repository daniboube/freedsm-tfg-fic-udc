import logging
import pynmea2

from ..schemas import Sensor, Attribute

# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-15s %(message)s')
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------

class NEO6MV2(Sensor):

    def __init__(self):
        super().__init__()
        self._device = self._open_port()
        self._attributes = [
            Attribute("loc", "location", "geo:json")
        ]


    def raw_read(self):
        # Load default values in case of error
        lng = 0.0
        lat = 0.0
    
        # Try to read the serial device
        try:

            # Reconnecting in case its needed
            if not self._device: 
                self._device = self._open_port()

            # Read until GPGLL field is found
            gpgll_found = False
            for _ in range(15):
                reading = self._device.readline()
                if reading:
                    reading = reading.decode("utf-8")
                    if reading.startswith("$GPGLL"):
                        gpgll_found = True
                        break

            # If GPGLL cannot be read, there is a problem with the GPS
            if not gpgll_found: raise IOError

            # Parse reading to get latitude and longitude
            gpgll = pynmea2.parse(reading)
            lng = gpgll.longitude
            lat = gpgll.latitude

        except Exception as e:
            if self._device: self._close_device()
            logger.info("Error while reading the GPS Neo6Mv2. Returning default values.")
            logger.error(str(e))

        return lng, lat

    
    def labeled_read(self):
        lng, lat = self.raw_read()
        if not lng and not lat: return {}
        output = {
            self._attributes[0].id: (lng, lat)
        }

        return output
