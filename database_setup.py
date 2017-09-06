#!/usr/bin/python2
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """"Class for the details of the user"""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(250), nullable=False)


class Genre(Base):
    """Class to implement the database for genre of tv series"""

    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    @property
    def serialize(self):
        """Return Data For JSON"""
        return {
            'name' : self.name,
            'id'   : self.id,
        }



class Tvseries(Base):
    """Class to implement the database for the tv series"""
    __tablename__ = 'tvseries'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(500), nullable=False)
    rating = Column(Integer)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    @property
    def serialize(self):
        """Return Data For JSON"""
        return {
            'name'          : self.name,
            'id'            : self.id,
            'description'   : self.description,
            'rating'        : self.rating,
        }


db_engine = create_engine('sqlite:///tvseries.db')


Base.metadata.create_all(db_engine)
