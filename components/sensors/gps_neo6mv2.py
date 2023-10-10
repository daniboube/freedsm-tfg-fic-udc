#
#  components/sensors/gps_neo6mv2.py - FreeDSM support for Raspberry PI
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
