# LiAn 433 sensors (tellstick duo)

This is a simple script for receiving input from devices to a tellstick duo and
passing it along to home assistant, using home assistants http/rest API.

It works by first configuring the devices in tellstick (`/etc/tellstick.conf`),
after figuring out the different sensors/buttons codes (house/unit etc), and
then update a config file that is read by this script and maps them to
a home assistant event.

For figuring out the devices different IDs/codes you can use this tool: https://github.com/magnushacker/tellcore-remote-spy.

## Enable http api in home assistant
In your configuration.yaml, add
```
http:
  api_password: YOUR-SUPER-SECRET-PASSWORD
```

## Installation
This assumes you use a raspberry pi (with hassbian).
You must have python and so on installed, and tellstick core.
Some help on installing the tellstick core software:

```
sudo sh -c 'echo "deb-src http://download.telldus.com/debian/ stable main" > /etc/apt/sources.list.d/telldus.list'
wget http://download.telldus.com/debian/telldus-public.key
sudo apt-key add telldus-public.key
sudo apt-get update
sudo apt-get install build-essential
sudo apt-get build-dep telldus-core
sudo apt-get install cmake libconfuse-dev libftdi-dev help2man
mkdir -p ~/tellstick-build
cd ~/tellstick-build
sudo apt-get --compile source telldus-core
sudo dpkg --install *.deb
```

Clone/download this repo. Install the dependencies by running

```
cd /path/to/lian-433-sensors
pip install -r requirements.txt
```

## Setup
### secrets.json
In the same directory as the script create `secrets.json` and set your password for
the http api above, like so:

```
{
  "ha_api_password": "YOUR-SUPER-SECRET-PASSWORD"
}
```
### config.json
In the same directory also create `config.json` and add the base url for your
home assistant api, like so:

```
{
  "api_base_url": "http://192.168.0.3:8123/api",
}
```

## Example configs
### tellstick.conf
```
device {
  id=1337
  name="Closet magnet"
  controller=0
  protocol="arctech"
  model="selflearning-switch"
  parameters {
    house="59069798"
    unit="5"
  }
}
```

### config.json
```
"sensor_mapping": {
  "1337": {
  "device_name": "closet_door",
  "friendly_name": "Closet door",
  "device_class": "door",
  "state_on": "on",
  "state_off": "off"
  }
}
```

## Running the script at boot (hassbian)
Creds to https://www.raspberrypi-spy.co.uk/2015/02/how-to-autorun-a-python-script-on-raspberry-pi-boot/

```
sudo nano /etc/profile
```

Add to the bottom:
```
sudo python /path/to/lian-433-sensors/sensors.py &
```

You'll probably also want to make the raspberry pi login on startup (to console)
to make the script run. I'm not super happy about having an auto logged in computer though but
I'll run with that until I do it in some better way...
To make ut autologin, open raspi-config;
```
sudo raspi-config
```
Select "Boot Options" then "Desktop/CLI" then "Console Autologin".