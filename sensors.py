#!/usr/bin/python3

import json
import requests

with open('secrets.json', 'r') as s:
    secrets = json.load(s)

with open('config.json', 'r') as c:
    config = json.load(c)


# closet door

# balcony button

device_name = 'closet_door'
friendly_name = 'Closet door'
device_class = 'door'
state = 'ON'

api_url = '{0}/states/binary_sensor.{1}'.format(config['api_base_url'], device_name)
payload = {'state': state, 'attributes': {
    'friendly_name': friendly_name, 
    'device_class': device_class}}

response = requests.post(
    api_url,
    headers={'x-ha-access': secrets['ha_api_password'], 'content-type': 'application/json'},
    data=json.dumps(payload))

print(response.text)