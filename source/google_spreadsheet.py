#!/usr/bin/python

# Google Spreadsheet DHT Sensor Data-logging Example

# Depends on the 'gspread' package being installed.  If you have pip installed
# execute:
#   sudo pip install gspread

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import time
import datetime
import logging

import Adafruit_DHT
import gspread

# Type of sensor, can be Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT_TYPE = Adafruit_DHT.DHT22

# Example of sensor connected to Raspberry Pi pin 23
DHT_PIN_AMBIENT  = 4
DHT_PIN_CURING  = 25
DHT_PIN_FRIDGE  = 24
# Example of sensor connected to Beaglebone Black pin P8_11
#DHT_PIN  = 'P8_11'

# Google Docs account email, password, and spreadsheet name.
GDOCS_EMAIL            = 'hewitson.is.me@gmail.com'
GDOCS_PASSWORD         = 'mjh590526'
GDOCS_SPREADSHEET_NAME = 'DHTHumidityLogs'
LOGFILE_NAME = 'Humiditylog.log'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 600

logging.basicConfig(filename=LOGFILE_NAME, level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logging.info('Starting up..')
 


def login_open_sheet(email, password, spreadsheet):
	while True:
		"""Connect to Google Docs spreadsheet and return the first worksheet."""
		try:
			gc = gspread.login(email, password)
			worksheet = gc.open(spreadsheet).sheet1#
			return worksheet
		except:
			logging.warning('Unable to login and get spreadsheet.  Check email, password, spreadsheet name.')
			time.sleep(300)


print 'Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)
print 'Press Ctrl-C to quit.'
worksheet = None
while True:
	# Login if necessary.
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_EMAIL, GDOCS_PASSWORD, GDOCS_SPREADSHEET_NAME)

	# Attempt to get sensor reading.
	humidity_ambient, temp_ambient = Adafruit_DHT.read(DHT_TYPE, DHT_PIN_AMBIENT)

	# Skip to the next reading if a valid measurement couldn't be taken.
	# This might happen if the CPU is under a lot of load and the sensor
	# can't be reliably read (timing is critical to read the sensor).
	if humidity_ambient is None or temp_ambient is None:
		time.sleep(2)
		continue

	# Attempt to get sensor reading.
	humidity_curing, temp_curing = Adafruit_DHT.read(DHT_TYPE, DHT_PIN_CURING)

	# Skip to the next reading if a valid measurement couldn't be taken.
	# This might happen if the CPU is under a lot of load and the sensor
	# can't be reliably read (timing is critical to read the sensor).
	if humidity_curing is None or temp_curing is None:
		time.sleep(2)
		continue

	# Attempt to get sensor reading.
	humidity_fridge, temp_fridge = Adafruit_DHT.read(DHT_TYPE, DHT_PIN_FRIDGE)

	# Skip to the next reading if a valid measurement couldn't be taken.
	# This might happen if the CPU is under a lot of load and the sensor
	# can't be reliably read (timing is critical to read the sensor).
	if humidity_fridge is None or temp_fridge is None:
		time.sleep(2)
		continue

#	print str(datetime.datetime.now())
	logging.info('Temperature: {0:0.1f} C'.format(temp_ambient))
	logging.info('Humidity:    {0:0.1f} %'.format(humidity_ambient))
	logging.info('Temperature: {0:0.1f} C'.format(temp_curing))
	logging.info('Humidity:    {0:0.1f} %'.format(humidity_curing))
	logging.info('Temperature: {0:0.1f} C'.format(temp_fridge))
	logging.info('Humidity:    {0:0.1f} %'.format(humidity_fridge))
 
	# Append the data in the spreadsheet, including a timestamp
	try:
		worksheet.append_row((datetime.datetime.now(), temp_ambient, humidity_ambient, temp_curing, humidity_curing, temp_fridge, humidity_fridge))
	except:
		# Error appending data, most likely because credentials are stale.
		# Null out the worksheet so a login is performed at the top of the loop.
		logging.error('Append error, logging in again')
		worksheet = None
		time.sleep(30)
		continue

	# Wait 30 seconds before continuing
	logging.info('Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME))
	time.sleep(FREQUENCY_SECONDS)
