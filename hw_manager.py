#
#  hw_manager.py - FreeDSM support for Raspberry PI
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

import subprocess
import logging

from components import SQM, TSL2591, AHT10
from components.sensors.gps_neo6mv2 import NEO6MV2
from components.sensors.mpu6050 import MPU6050

# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-15s %(message)s')
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------

class HardwareManager:

    # Hardware info
    _device_id = None
    _device_tz = None

    # Components
    _light_sensor = None
    _sqm = None
    _ambiance = None
    _gyro = None
    _gps = None

    # Stored attributes
    _freedsm_attrs = None
    _sqm_attrs = None

    def __init__(self):
        self._device_id = subprocess.check_output(["cat", "/etc/machine-id"]).decode("utf8")[:-1]
        self._device_tz = subprocess.check_output(["cat", "/etc/timezone"]).decode("utf8")[:-1]
        self._freedsm_attrs = []
        self._sqm_attrs = []

    
    @property
    def device_id(self):
        return self._device_id

    
    @property
    def device_tz(self):
        return self._device_tz

    
    @property
    def freedsm_attrs(self):
        return self._freedsm_attrs

    
    @property
    def sqm_attrs(self):
        return self._sqm_attrs


    def scan(self):
        errors = []

        try: # Get TSL2591
            self._light_sensor = TSL2591()
        except Exception as e:
            errors.append("Missing Light Sensor TSL2591")
            logger.error(str(e))

        try: # Get SQM LU-DL
            self._sqm = SQM()
        except Exception as e:
            errors.append("Missing SQM LU-DL")
            logger.error(str(e))

        if errors:
            return False, errors

        commom_attrs = []
        self._freedsm_attrs = self._light_sensor.get_attributes()
        self._sqm_attrs = self._sqm.get_attributes()

        try: # Get AHT10
            self._ambiance = AHT10()
            commom_attrs += self._ambiance.get_attributes()
        except Exception as e:
            logger.info("AHT10 sensor not detected")

        try: # Get Gyroscope MPU6050
            self._gyro = MPU6050()
            commom_attrs += self._gyro.get_attributes()
        except Exception as e:
            logger.info("Gyroscope MPU6050 not detected")

        try: # Get GPS NEO6Mv2
            self._gps = NEO6MV2()
            commom_attrs += self._gps.get_attributes()
        except Exception as e:
            logger.info("GPS NEO6Mv2 not detected")
            logger.info("Forcing null GPS Position")
            commom_attrs += [{"object_id": "loc", "name": "location", "type": "geo:json"}]

        self._freedsm_attrs += commom_attrs
        self._sqm_attrs += commom_attrs

        return True, errors


    def read_freedsm(self):
        readings = self._light_sensor.labeled_read()
        readings = readings | self._ambiance.labeled_read() if self._ambiance else readings
        return readings


    def read_sqm(self):
        readings = self._sqm.labeled_read()
        readings = readings | self._ambiance.labeled_read() if self._ambiance else readings
        return readings


    def read_one_shot_sensors(self):
        readings = {}
        readings = readings | self._gyro.labeled_read() if self._gyro else readings
        readings = readings | self._gps.labeled_read() if self._gps else readings
        return readings
    

    def get_freedsm_logging_headers(self):
        attrs = self._light_sensor.get_attributes()
        attrs += self._ambiance.get_attributes() if self._ambiance else []
        return attrs


    def get_sqm_logging_headers(self):
        attrs = self._sqm.get_attributes()
        attrs += self._ambiance.get_attributes() if self._ambiance else []
        return attrs


    def configure_light_sensor(self, gain=None, integration=None):
        if gain: self._light_sensor.set_gain_level(gain)
        if integration: self._light_sensor.set_integration_level(integration)
        return
        