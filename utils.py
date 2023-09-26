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