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

@app.route('/home/genre/<int:genre_id>/JSON')
def genreJSON(genre_id):
    """Funtion to return JSON data for Genre"""
    tvseriesquery = session.query(Tvseries).filter_by(genre_id = genre_id).all()
    return jsonify(Tvseries=[i.serialize for i in tvseriesquery])

@app.route('/home/tvseries/<int:tvseries_id>/JSON')
def tvseriesJSON(tvseries_id):
    """Funtion to return JSON data for Genre"""
    tvseriesquery = session.query(Tvseries).filter_by(id = tvseries_id).one()
    return jsonify( tvseriesquery =tvseriesquery.serialize)



@app.route('/')
@app.route('/home')
def index():
    """"index page for the wesite """
    genrequery = session.query(Genre).all()
    tvseriesquery = session.query(Tvseries).order_by(desc(Tvseries.id)).limit(10).all()
    return render_template('index.html', genres = genrequery,tvseries = tvseriesquery)



@app.route('/home/genre/<int:genre_id>/')
def genre(genre_id):
    """"genre page for the wesite """
    genrequery = session.query(Genre).filter_by(id = genre_id).one()
    tvseriesquery = session.query(Tvseries).filter_by(genre_id = genre_id).all()
    return render_template('genre.html',genre = genrequery, tvseries = tvseriesquery)


@app.route('/home/tvseries/<int:tvseries_id>')
def tvseries(tvseries_id):
    """"genre page for the wesite """
    tvseriesquery = session.query(Tvseries).filter_by(id = tvseries_id).one()
    return render_template('tvseries.html',tvseries = tvseriesquery)



@app.route('/home/tvseries/add',methods=['GET','POST'])
def add_tvseries():
    """"page to add new tv series for the wesite"""
    if request.method == 'POST':
        newTvseries = Tvseries(name = request.form['name'], rating = request.form['rating'], description = request.form['description'], genre_id = request.form['genre_id'])
        session.add(newTvseries)
        flash("New Tvseries Successfully Added")
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('addtvseries.html')



@app.route('/home/tvseries/<int:tvseries_id>/edit',methods=['GET','POST'])
def edit_tvseries(tvseries_id):
    """"page to edit tv series for the wesite"""
    editedTvseries = session.query(Tvseries).filter_by(id = tvseries_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedTvseries.name = request.form['name']
        if request.form['rating']:
            editedTvseries.rating = request.form['rating']
        if request.form['description']:
            editedTvseries.description = request.form['description']
        if request.form['genre_id']:
            editedTvseries.genre_id = request.form['genre_id']
        session.add(editedTvseries)
        flash("%s Successfully Edited" % editedTvseries.name)
        session.commit()
        return redirect(url_for('tvseries',tvseries_id = tvseries_id))
    else:
        return render_template('edittvseries.html',tvseries = editedTvseries)



@app.route('/home/tvseries/<int:tvseries_id>/delete',methods=['GET','POST'])
def delete_tvseries(tvseries_id):
    """"page to delete tv series for the wesite"""
    tvseriesDelete = session.query(Tvseries).filter_by(id = tvseries_id).one()
    if request.method == 'POST':
        session.delete(tvseriesDelete)
        flash("%s Successfully Deleted" % tvseriesDelete.name)
        session.commit
        return redirect(url_for('index'))
    else :
        return render_template('deletetvseries.html',tvseries = tvseriesDelete)


if __name__ == '__main__':
    app.secret_key = 'my_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
