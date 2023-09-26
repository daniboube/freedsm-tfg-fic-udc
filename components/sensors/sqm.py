import logging
import serial

from ..schemas import Sensor, Attribute

# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-15s %(message)s')
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------

class SQM(Sensor):

    def __init__(self):
        super().__init__()
        self._device = self._open_port()
        self._attributes = [
            Attribute("m", "mpsas", "Float"),
            Attribute("f", "frequency", "Float"),
            Attribute("c", "periodCounts", "Float"),
            Attribute("s", "periodSeconds", "Float")
        ]


    def raw_read(self):
        # Load default values in case of error
        mpsas = 0.0
        freq = 0.0
        p_counts = 0.0
        p_seconds = 0.0

        try: # Try to read the serial device
            
            # Reconnecting in case its needed
            if not self._device: 
                self._device = self._open_port()

            self._device.write(b"rx\r\n")
            reading = self._device.readline()

            if reading: 
                reading = reading.decode("utf8")
                mpsas = float(reading[2:8].strip())
                freq = float(reading[10:20].strip())
                p_counts = float(reading[23:33].strip())
                p_seconds = float(reading[35:46].strip())

        except Exception as e:
            # Force to reconnect on the next try
            self._device = None
            logger.info("Error while reading the SQM sensor. Returning default values.")
            logger.error(str(e))

        return mpsas, freq, p_counts, p_seconds

    
    def _open_port(self):
        return serial.Serial(
            port="/dev/ttyUSB0",
            baudrate=115200,
            bytesize=8,
            timeout=3,
            stopbits=serial.STOPBITS_ONE)

