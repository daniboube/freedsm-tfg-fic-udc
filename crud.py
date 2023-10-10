#
#  crud.py - FreeDSM support for Raspberry PI
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

import requests
import settings

# -----------------------------------------------------------------------------

def get_device_by_id(device_id: str, type: str):
    path = f"http://{settings.IOT_AGENT_HOST}:{settings.IOT_AGENT_PORT}/iot/devices/{device_id}"
    headers = {"fiware-service": "g4s", "fiware-servicepath": f"/{type.lower()}"}
    response = requests.get(path, headers=headers)
    
    if response.status_code == 404:
        return None

    response.raise_for_status()
    return response.content


def create_device(device_id: str, type: str, timezone: str, attributes: list, static: list=None, lazy: list=None, commands: list=None):
    body = {
        "devices": [
            {
                "device_id": device_id,
                "entity_name": device_id,
                "entity_type": type,
                "protocol": "PDI-IoTA-UltraLight",
                "transport": "MQTT",
                "timezone": timezone,
                "attributes": attributes  
            }
        ]
    }

    # Optional attributes
    if static: body["static_attributes"] = static
    if lazy: body["lazy"] = lazy
    if commands: body["commands"] = commands

    path = f"http://{settings.IOT_AGENT_HOST}:{settings.IOT_AGENT_PORT}/iot/devices"
    headers = {"fiware-service": "g4s", "fiware-servicepath": f"/{type.lower()}"}
    response = requests.post(path, headers=headers, json=body)
    response.raise_for_status()
    
    return response.content


def update_device(device_id: str, type: str, timezone: str=None, attributes: list=None, static: list=None, lazy: list=None, commands: list=None):
    body = {}
    if timezone: body["timezone"] = timezone
    if attributes: body["attributes"] = attributes
    if static: body["static_attributes"] = static
    if lazy: body["lazy"] = lazy
    if commands: body["commands"] = commands

    path = f"http://{settings.IOT_AGENT_HOST}:{settings.IOT_AGENT_PORT}/iot/devices/{device_id}"
    headers = {"fiware-service": "g4s", "fiware-servicepath": f"/{type.lower()}"}
    response = requests.put(path, headers=headers, json=body)
    response.raise_for_status()
    
    return response.content