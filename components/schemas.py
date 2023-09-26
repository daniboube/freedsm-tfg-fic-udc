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
        