#!/usr/bin/python3

import json
import requests
import time
import tellcore.telldus as td
import tellcore.constants as const

# Read secrets
with open('secrets.json', 'r') as s:
    secrets = json.load(s)

# Read config
with open('config.json', 'r') as c:
    config = json.load(c)

# sensor config. The keys are the id from the tellstick config and the value are the data for home assistant.
sensor_mapping = config["sensor_mapping"]

METHODS = {const.TELLSTICK_TURNON: 'turn on',
           const.TELLSTICK_TURNOFF: 'turn off',
           const.TELLSTICK_BELL: 'bell',
           const.TELLSTICK_TOGGLE: 'toggle',
           const.TELLSTICK_DIM: 'dim',
           const.TELLSTICK_LEARN: 'learn',
           const.TELLSTICK_EXECUTE: 'execute',
           const.TELLSTICK_UP: 'up',
           const.TELLSTICK_DOWN: 'down',
           const.TELLSTICK_STOP: 'stop'}

# lastClick = time.time()

def event(id, method, data, cid):
    method_string = METHODS.get(method, "UNKNOWN METHOD {0}".format(method))
    id_str = str(id)

    if id_str in sensor_mapping:
        sensor = sensor_mapping[id_str]
        # print(sensor)
        if method == const.TELLSTICK_TURNON:
            print('turn on!')
        elif method == const.TELLSTICK_TURNOFF:
            print('turn off!')


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


# device_name = 'closet_door'
# friendly_name = 'Closet door'
# device_class = 'door'
# state = 'ON'

# api_url = '{0}/states/binary_sensor.{1}'.format(config['api_base_url'], device_name)
# payload = {'state': state, 'attributes': {
#     'friendly_name': friendly_name, 
#     'device_class': device_class}}

# response = requests.post(
#     api_url,
#     headers={'x-ha-access': secrets['ha_api_password'], 'content-type': 'application/json'},
#     data=json.dumps(payload))

# print(response.text)
