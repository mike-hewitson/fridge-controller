#!/usr/bin/env python
import web
import xml.etree.ElementTree as ET
import sys
import time
import datetime
import logging

import Adafruit_DHT

# Type of sensor, can be Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT_TYPE = Adafruit_DHT.DHT22

# Example of sensor connected to Raspberry Pi pin 23
DHT_PIN_AMBIENT  = 4
DHT_PIN_CURING  = 25
DHT_PIN_FRIDGE  = 24
LOGFILE_NAME = 'RestService.log'
DHT_SENSORS = {"Fridge":DHT_PIN_FRIDGE, "Ambient":DHT_PIN_AMBIENT, "Curing":DHT_PIN_CURING}

logging.basicConfig(filename=LOGFILE_NAME, level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logging.info('Starting up..')

tree = ET.parse('user_data.xml')
root = tree.getroot()

print tree
print root

urls = (
    '/sensors', 'list_sensors',
    '/sensors/(.*)', 'get_sensor'
)

app = web.application(urls, globals())

class list_sensors:        
    def GET(self):
        output = 'sensors:[';
        for child in root:
                print 'child', child.tag, child.attrib
                output += str(child.attrib) + ','
        output += ']';
        return output

class get_sensor:
    def GET(self, sensor):
        for child in root:
                if child.attrib['id'] == sensor:
                    return str(child.attrib)

if __name__ == "__main__":
    app.run()


    # Attempt to get sensor reading.
    humidity_ambient, temp_ambient = Adafruit_DHT.read(DHT_TYPE, DHT_PIN_AMBIENT)

    # Skip to the next reading if a valid measurement couldn't be taken.
    # This might happen if the CPU is under a lot of load and the sensor
    # can't be reliably read (timing is critical to read the sensor).
    if humidity_ambient is None or temp_ambient is None:
        time.sleep(2)

    # Attempt to get sensor reading.
    humidity_curing, temp_curing = Adafruit_DHT.read(DHT_TYPE, DHT_PIN_CURING)

    # Skip to the next reading if a valid measurement couldn't be taken.
    # This might happen if the CPU is under a lot of load and the sensor
    # can't be reliably read (timing is critical to read the sensor).
    if humidity_curing is None or temp_curing is None:
        time.sleep(2)

    # Attempt to get sensor reading.
    humidity_fridge, temp_fridge = Adafruit_DHT.read(DHT_TYPE, DHT_PIN_FRIDGE)

    # Skip to the next reading if a valid measurement couldn't be taken.
    # This might happen if the CPU is under a lot of load and the sensor
    # can't be reliably read (timing is critical to read the sensor).
    if humidity_fridge is None or temp_fridge is None:
        time.sleep(2)
 
#   print str(datetime.datetime.now())
    logging.info('Temperature: {0:0.1f} C'.format(temp_ambient))
    logging.info('Humidity:    {0:0.1f} %'.format(humidity_ambient))
    logging.info('Temperature: {0:0.1f} C'.format(temp_curing))
    logging.info('Humidity:    {0:0.1f} %'.format(humidity_curing))
    logging.info('Temperature: {0:0.1f} C'.format(temp_fridge))
    logging.info('Humidity:    {0:0.1f} %'.format(humidity_fridge))
 

