#!/usr/bin/python3

import json

with open("secrets.json") as f:
    data = json.load(f)

print(data["ha_api_password"])

# closet door

# balcony button

