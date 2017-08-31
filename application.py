#!/usr/bin/python2
from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    """"index page for the wesite """
    return "home page"


@app.route('/genre')
@app.route('/home/genre')
def genre():
    """"genre page for the wesite """
    return "genre page"


@app.route('/genre/tvseries')
@app.route('/home/genre/tvseries')
def tvseries():
    """"genre page for the wesite """
    return "tvseries page"


@app.route('/genre/tvseries/add')
@app.route('/home/genre/tvseries/add')
def add_tvseries():
    """"page to add new tv series for the wesite"""
    return "add page"


@app.route('/genre/tvseries/edit')
@app.route('/home/genre/tvseries/edit')
def edit_tvseries():
    """"page to edit tv series for the wesite"""
    return "edit page"


@app.route('/genre/tvseries/delete')
@app.route('/home/genre/tvseries/delete')
def delete_tvseries():
    """"page to delete tv series for the wesite"""
    return "delete page"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
