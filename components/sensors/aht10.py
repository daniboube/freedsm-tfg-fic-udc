#
#  components/sensors/aht10.py - FreeDSM support for Raspberry PI
#
#
#  FreeDSM:
#  Copyrigth (C) 2022  Daniel Boubeta Portela
#                      José Carlos Dafonte Vázquez
#                      
#  University of A Coruña (UDC), Galicia, Spain
#  Developed as a part of the Gaia4Sustainability (G4S) project
#  <http://gaia4sustainability.eu/>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

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
        