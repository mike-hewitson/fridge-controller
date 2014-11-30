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
DHT_SENSORS = {"Fridge": DHT_PIN_FRIDGE, "Ambient": DHT_PIN_AMBIENT, "Curing": DHT_PIN_CURING}

logging.basicConfig(filename=LOGFILE_NAME, level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logging.info('Starting up..')

print DHT_SENSORS

urls = (
    '/sensors', 'list_sensors',
    '/sensors/(.*)', 'get_sensor'
)

app = web.application(urls, globals())

class list_sensors:        
    def GET(self):
        output = 'sensors:[';
        for sensor, pin in DHT_SENSORS.items():
            logging.info('List - Sensor:' + sensor + ' Pin; ' + str(pin))
            humidity, temp = Adafruit_DHT.read(DHT_TYPE, pin)
            if humidity is None or temp is None:
                logging.info('Data not returned') 
                time.sleep(2)
            print 'sensor', sensor, datetime.datetime.now(), temp, humidity
            logging.info('List - Temperature: {0:0.1f} C'.format(temp))
            logging.info('List - Humidity:    {0:0.1f} %'.format(ambient))
            output += "{'sensor': '" + Sensor + "'temp': '" + str(temp) + "'},"
        output += ']';
        return output

class get_sensor:
    def GET(self, sensor):
        for sensor in DHT_SENSORS:
            if child.attrib['id'] == sensor:
                return str("bob")

if __name__ == "__main__":
    app.run()

