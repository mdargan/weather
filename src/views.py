import datetime
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession as db,
    City,
    WeatherRecord
)

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def home(request):
    try:
        cities = db.query(City).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return { 'cities': cities }


@view_config(renderer="json_custom", name="city_stats.json")
def city_stats_view(request):

    try:
        city_param = request.GET.setdefault('city', 'Moscow')
        city = db.query(City).filter(City.name == city_param).first()
                   
        sql = """
            SELECT streak,
            start,
            start + streak as end
            FROM (SELECT date,
                lead(date)  OVER (ORDER BY date) - date streak,
                since_previous,
                before_next,
                date as start
                FROM (SELECT date, is_clear,
                       date - lag(date) OVER (ORDER BY date) since_previous,
                       lead(date) OVER (ORDER BY date) - date before_next
                       FROM weather_record
                       WHERE city_id = :city_id 
                       AND is_clear = 't'
                       AND date BETWEEN :start_date AND :end_date
                     ) dt 
                
		) dd 
        WHERE streak IS NOT NULL
        ORDER BY streak desc;
        """
		
        result = { 
            "result": "ok", 
            "list" : { }
        }

        #find the oldest weather record
        start_date = db.query(WeatherRecord).first().date
        end_date = datetime.date.today()                          

        #get overall longest clear sky period 
        overall = db.query("start", "end", "streak").from_statement(sql).params(city_id=city.id,
        start_date=start_date, end_date=end_date).first()
       
        if overall:
            result["list"]["overall"] = overall	

        #Current month clear sky period
        start_date =  datetime.date.today().replace(day=1)
        month_all = db.query("start", "end", "streak").from_statement(sql).params(city_id=city.id,
        start_date=start_date, end_date=end_date).all()
        
        if month_all:
            result["list"]["month"] = month[0]

        current_period = None        
              
        #Determine if current date falls into any current month's clear streak
        for period in month_all:
            if period[0] <= datetime.date.today() <= period[1]:
                current_period = period
                break

        if current_period is not None:
            result["list"]["current"] = current_period                

        return result

    except DBAPIError as e:
        #return { "result" : "error" }
        pass
        

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_src_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

