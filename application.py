#!/usr/bin/python2
from flask import Flask, url_for,render_template
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    """"index page for the wesite """
    return render_template('index.html')


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
