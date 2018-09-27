#!/usr/bin/python3
import json
import requests
import time
import tellcore.telldus as td
import tellcore.constants as const
import os

script_path = os.path.abspath(os.path.dirname(__file__))
secrets_path = os.path.join(script_path, 'secrets.json')
config_path = os.path.join(script_path, 'config.json')

# Read secrets
with open(secrets_path, 'r') as s:
    secrets = json.load(s)

# Read config
with open(config_path, 'r') as c:
    config = json.load(c)

# sensor config. The keys are the id from the tellstick config
# and the value are the data for home assistant.
sensor_mapping = config["sensor_mapping"]

last_event_time = time.time()
last_event = ""


def event(id, method, data, cid):
    id_str = str(id)

    if id_str in sensor_mapping:
        sensor = sensor_mapping[id_str]
        payload = {
            'state': '',
            'attributes': {
                'friendly_name': sensor['friendly_name'],
                'device_class':  sensor['device_class']
            }
        }
        if method == const.TELLSTICK_TURNON:
            payload['state'] = sensor['state_on']
        elif method == const.TELLSTICK_TURNOFF:
            payload['state'] = sensor['state_off']

        api_url = '{0}/states/binary_sensor.{1}'.format(
            config['api_base_url'],
            sensor['device_name'])

        requests.post(
            api_url,
            headers={
                'x-ha-access': secrets['ha_api_password'],
                'content-type': 'application/json'
            },
            data=json.dumps(payload))


try:
    import asyncio
    loop = asyncio.get_event_loop()
    dispatcher = td.AsyncioCallbackDispatcher(loop)
    core = td.TelldusCore(callback_dispatcher=dispatcher)
except ImportError:
    loop = None
    core = td.TelldusCore()

core.register_device_event(event)

try:
    if loop:
        loop.run_forever()
    else:
        import time
        while True:
            core.callback_dispatcher.process_pending_callbacks()
            time.sleep(0.5)
except KeyboardInterrupt:
    pass
