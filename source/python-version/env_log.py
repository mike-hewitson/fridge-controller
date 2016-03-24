import sqlite3
# import sys
import Adafruit_DHT
import logging
import datetime
from pymongo import MongoClient

LOGFILE_NAME = '/var/log/sensor.log'

logging.basicConfig(filename=LOGFILE_NAME, level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s:%(message)s')
logging.info('Recording started')
logging.info('Logging into sqlite')


def log_values(sensor_id, temp, hum):
    # It is important to provide an
    conn = sqlite3.connect('/var/www/lab_app/lab_app.db')
    # absolute path to the database
    # file, otherwise Cron won't be
    # able to find it!
    curs = conn.cursor()
    curs.execute("""INSERT INTO temperatures values(datetime('now'),
         (?), (?))""", (sensor_id, temp))
    curs.execute("""INSERT INTO humidities values(datetime('now'),
         (?), (?))""", (sensor_id, hum))
    conn.commit()
    conn.close()

amb_humidity, amb_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
if amb_humidity is not None and amb_temperature is not None:
    log_values("Ambient", amb_temperature, amb_humidity)
else:
    logging.warning('Sensor {0} reading failed.'.format('Ambient'))

fridge_humidity, fridge_temperature = Adafruit_DHT.read_retry(
    Adafruit_DHT.DHT22, 24)
if fridge_humidity is not None and fridge_temperature is not None:
    log_values("Fridge", fridge_temperature, fridge_humidity)
else:
    logging.warning('Sensor {0} reading failed.'.format('Fridge'))

curing_humidity, curing_temperature = Adafruit_DHT.read_retry(
    Adafruit_DHT.DHT22, 25)
if curing_humidity is not None and curing_temperature is not None:
    log_values("Curing", curing_temperature, curing_humidity)
else:
    logging.warning('Sensor {0} reading failed.'.format('Curing'))

logging.info('Logging into mongo')

client = MongoClient()
db = client.charcuterie
reading = {'date': datetime.datetime.utcnow(), 'sensors': [
    {'sensor': 'Ambient', 'temp': amb_temperature, 'hum': amb_humidity},
    {'sensor': 'Fridge', 'temp': fridge_temperature, 'hum': fridge_humidity},
    {'sensor': 'Curing', 'temp': curing_temperature, 'hum': curing_humidity},
]}
readings = db.readings

reading_id = readings.insert_one(reading).inserted_id


logging.info('Recording ended')
