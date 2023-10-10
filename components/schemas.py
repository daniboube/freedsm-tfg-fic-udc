#
#  components/schemas.py - FreeDSM support for Raspberry PI
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

from abc import ABC, abstractclassmethod

# -----------------------------------------------------------------------------

class Sensor(ABC):

    _device = None
    _attributes = None
    
    def get_attributes(self):
        output = []
        [output.append(attr.as_json()) for attr in self._attributes]
        return output


    @abstractclassmethod
    def raw_read(self):
        raise NotImplementedError

    
    def labeled_read(self):
        attr_ids = []

        # Get a list of object_ids from all the attributes and raw readings
        [attr_ids.append(attr.id) for attr in self._attributes]
        readings = list(self.raw_read())  
          
        # Map an object_id to a reading value
        return dict(zip(attr_ids, readings))


# -----------------------------------------------------------------------------

class Attribute:

    _id = None
    _name = None
    _type = None

    def __init__(self, id: str, name: str, type: str):
        self._object_id = id
        self._name = name
        self._type = type

    
    @property
    def id(self):
        return self._object_id

    
    @property
    def name(self):
        return self._name

    
    @property
    def type(self):
        return self._type


    def as_json(self):
        return {
            "object_id": self._object_id,
            "name": self._name,
            "type": self._type
        }
        