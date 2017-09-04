from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Tvseries


# Connect to Database and create database session
engine = create_engine('sqlite:///tvseries.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

tvseriesquery = session.query(Tvseries).order_by(desc(Tvseries.id)).limit(10).all()

for i in tvseriesquery:
    print("Name:{name} genre:{rating}".format(name=i.name, rating=i.genre.name))
    tvseriesquery = session.query(Tvseries).order_by(desc(Tvseries.id)).limit(10).all()
    , tvseries = tvseriesquery