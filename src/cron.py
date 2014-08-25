import os
import json
import datetime
import time
from urllib.request import urlopen

from paste.deploy import appconfig
 
from sqlalchemy import engine_from_config, func
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
 
#Import sqlalchemy objects
from models import DBSession as db, City, WeatherRecord
 
#import the session manager. This way commits will be handled automatically by the Zope Transaction Manager
import transaction

 
# Load Application Configuration and Return as Dictionary
conf = appconfig('config:' + '../development.ini', 
       name="main", relative_to=os.getcwd())
 
#configure SQLAlchemy engine 
engine = engine_from_config(conf, 'sqlalchemy.')
db.configure(bind=engine)
 

def update_weather_data(city_id, start_dt):
    
    timestamp = time.mktime(start_dt.timetuple()) 
    api_url = 'http://api.openweathermap.org/data/2.5/history/city?id=%d&type=day&start=%d' % (city_id, timestamp)
    response = urlopen(api_url)
    data = json.loads(response.read().decode())

    conditions = { }
 
    for d in data['list']:
        dt = datetime.datetime.fromtimestamp(int(d['dt'])).date()
        cond = d['weather'][0]['main']
        conditions.setdefault(dt, []).append(cond)

    with transaction.manager:
        for k in conditions:
            cds = set(conditions[k])
            is_clear = len(cds) == 1 and 'Clear' in cds
            record = WeatherRecord(date=k, is_clear=is_clear)
            db.add(record)    
	       

count = db.query(func.count(WeatherRecord.id)).first()[0] 
start_date = datetime.date.today()

if count == 0:
    #We assume we running first time since database is empty
    #and will load all records for last year
    start_date = start_date - datetime.timedelta(days=365)

else:
	#Perform incremental update from latest record
    latest = db.query(WeatherRecord).order_by(WeatherRecord.date).first()
    start_date = latest.date

cities = db.query(City).all()
for c in cities:    
    update_weather_data(c.owm_id, start_date)	
	
	
 

