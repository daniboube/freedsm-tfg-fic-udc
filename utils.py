#
#  utils.py - FreeDSM support for Raspberry PI
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

import json
import settings

# -----------------------------------------------------------------------------

def json2ultralight(readings):
    parsed_readings = ""
    for attr_id, attr_value in readings.items():
        if type(attr_value) is not str: attr_value = json.dumps(attr_value)
        attr_value = attr_value.replace(')', '').replace('(', '').replace(' ', '')
        parsed_readings += f"{attr_id}|{attr_value}|"
    return parsed_readings[:-1]