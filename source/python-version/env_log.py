import sqlite3
import sys
import Adafruit_DHT
import logging

LOGFILE_NAME		= '/var/log/sensor.log'

logging.basicConfig(filename=LOGFILE_NAME, level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logging.info('Recording started')


def log_values(sensor_id, temp, hum):
	conn=sqlite3.connect('/var/www/lab_app/lab_app.db')  #It is important to provide an
							     #absolute path to the database
							     #file, otherwise Cron won't be
							     #able to find it!
	curs=conn.cursor()
	curs.execute("""INSERT INTO temperatures values(datetime('now'),
         (?), (?))""", (sensor_id,temp))
	curs.execute("""INSERT INTO humidities values(datetime('now'),
         (?), (?))""", (sensor_id,hum))
	conn.commit()
	conn.close()

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
if humidity is not None and temperature is not None:
	log_values("Ambient", temperature, humidity)	
else:
	logging.warning('Sensor {0} reading failed.'.format('Ambient'))

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 24)
if humidity is not None and temperature is not None:
	log_values("Fridge", temperature, humidity)	
else:
	logging.warning('Sensor {0} reading failed.'.format('Fridge'))

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 25)
if humidity is not None and temperature is not None:
	log_values("Curing", temperature, humidity)	
else:
	logging.warning('Sensor {0} reading failed.'.format('Curing'))

logging.info('Recording ended')
