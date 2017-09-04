#!/usr/bin/python2
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Tvseries


#Connect to Database and create database session
engine = create_engine('sqlite:///tvseries.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
@app.route('/')
@app.route('/home')
def index():
    """"index page for the wesite """
    genrequery = session.query(Genre).all()
    tvseriesquery = session.query(Tvseries).order_by(desc(Tvseries.id)).limit(10).all()
    return render_template('index.html', genres = genrequery,tvseries = tvseriesquery)


@app.route('/genre')
@app.route('/home/genre')
def genre():
    """"genre page for the wesite """
    return render_template('genre.html')


@app.route('/genre/tvseries')
@app.route('/home/genre/tvseries')
def tvseries():
    """"genre page for the wesite """
    return render_template('tvseries.html')


@app.route('/genre/tvseries/add')
@app.route('/home/genre/tvseries/add')
def add_tvseries():
    """"page to add new tv series for the wesite"""
    return render_template('addtvseries.html')


@app.route('/genre/tvseries/edit')
@app.route('/home/genre/tvseries/edit')
def edit_tvseries():
    """"page to edit tv series for the wesite"""
    return render_template('edittvseries.html')


@app.route('/genre/tvseries/delete')
@app.route('/home/genre/tvseries/delete')
def delete_tvseries():
    """"page to delete tv series for the wesite"""
    return render_template('deletetvseries.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
