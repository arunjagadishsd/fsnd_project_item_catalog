from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Tvseries


# Connect to Database and create database session
engine = create_engine('sqlite:///tvseries.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

genre = session.query(Genre).all()
tvseriesquery = tvseriesquery = session.query(Tvseries).filter_by(id = 1).one()

print (tvseriesquery.name)

