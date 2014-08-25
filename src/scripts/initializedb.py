import os
import sys
import transaction
import datetime
import random

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    City,
	WeatherRecord,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

CITIES = { 
    "Moscow" : 524901,
    "Salt Lake City" : 5780993,
    "Vladivostok" : 2013348,
    "Prague" : 3067696
}

def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

	#Generate fake statistics for 1 year
    DAYS = 365 * 1

    #Init database with example list of cities
    with transaction.manager:
        for c in CITIES:
            city = City(name=c, owm_id=CITIES[c])
            DBSession.add(city)
            DBSession.flush()
            print("Added city: " + city.name)            
            prev_y = datetime.datetime.now() - datetime.timedelta(DAYS)
            
            for d in (prev_y + datetime.timedelta(n) for n in range(DAYS)):
                is_clear = bool(random.getrandbits(1))
                wr = WeatherRecord(city=city.id, date=d, is_clear=is_clear)
                DBSession.add(wr)
                print("Added weather record: " + str(wr.date) + " " + str(wr.is_clear))                
            DBSession.flush()
