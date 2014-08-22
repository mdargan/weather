from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
	Date,
	ForeignKey,
    Boolean
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class City(Base):
    __tablename__ = 'city'
    
    id = Column('city_id', Integer, primary_key=True)
    name = Column('name', Text)
    owm_id = Column('owm_id', Integer)

class WeatherRecord(Base):
    __tablename__ = 'weather_record'
    
    id = Column('record_id', Integer, primary_key=True)
    date = Column('date', Date)
    is_clear = Column('is_clear', Boolean)
    city = Column('city_id', Integer, 
		ForeignKey('city.city_id', use_alter=True, name='fk_city_id')
    )

