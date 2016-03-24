import datetime
from pymongo import MongoClient
client = MongoClient()
db = client.charcuterie
reading = {'date': datetime.datetime.utcnow(), 'sensors': [
    {'sensor': 'Ambient', 'temp': 25.4, 'hum': 23.11},
    {'sensor': 'Fridge', 'temp': 26.4, 'hum': 24.11},
    {'sensor': 'Curing', 'temp': 27.4, 'hum': 25.11},
]}
readings = db.readings

reading_id = readings.insert_one(reading).inserted_id
