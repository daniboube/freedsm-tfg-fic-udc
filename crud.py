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