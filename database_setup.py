#!/usr/bin/python3
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Genre(Base):
    """Class to implement the database for genre of tv series"""

    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class Tvseries(Base):
    """Class to implement the database for the tv series"""
    __tablename__ = 'tvseries'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250), nullable=False)
    rating = Column(String(50))
    category_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)


db_engine = create_engine('sqlite:///tvseries.db')


Base.metadata.create_all(db_engine)
