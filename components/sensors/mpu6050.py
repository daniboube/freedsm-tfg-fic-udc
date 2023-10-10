#
#  components/sensors/mpu6050.py - FreeDSM support for Raspberry PI
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
import math
import time
import adafruit_mpu6050

from adafruit_extended_bus import ExtendedI2C
from ..schemas import Sensor, Attribute

# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-15s %(message)s')
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------

class MPU6050(Sensor):

    def __init__(self):
        self._device = adafruit_mpu6050.MPU6050(ExtendedI2C(3))
        self._attributes = [
            Attribute("inc", "inclination", "Object")
        ]

    
    def raw_read(self):
        # Load default values in case of error
        angle_x = 0.0
        angle_y = 0.0

        # Try to read the i2c device
        try:
            self._device.sleep = False
            ax, ay, az = self._average_acelaration(20, 0.250)
            vector_mag = math.sqrt(ax*ax + ay*ay + az*az)
            rad2degree= 180 / math.pi

            angle_x = round(rad2degree * math.asin(ax / vector_mag), 5)
            angle_y = round(rad2degree * math.asin(ay / vector_mag), 5)

            self._device.sleep = True
        except Exception as e:
            logger.info("Error while reading the MPU6050 sensor. Returning default values.")
            logger.error(str(e))

        return angle_x, angle_y


    def _average_acelaration(self, count, timing_ms):
        gx = 0
        gy = 0
        gz = 0
        gxoffset =  0.07
        gyoffset = -0.04

        for _ in range(count):
            ax, ay, az = self._device.acceleration
            gx += ax - gxoffset
            gy += ay - gyoffset
            gz += az
            time.sleep(timing_ms)
        return gx/count, gy/count, gz/count

    
    def labeled_read(self):
        angle_x, angle_y = self.raw_read()
        output = {
            self._attributes[0].id: {
                "angleX": angle_x,
                "angleY": angle_y
            }
        }

        return output
