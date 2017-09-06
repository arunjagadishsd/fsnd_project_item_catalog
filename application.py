#!/usr/bin/python2
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash  # noqa

# imports for the login
from flask import session as login_session
import string
import random
# from OAuth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
# imports for Databse
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Tvseries
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"
# Connect to Database and create database session
engine = create_engine('sqlite:///tvseries.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                    'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome to the Tvseries page'
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output
# to logout from the page


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/home/genre/<int:genre_id>/JSON')
def genreJSON(genre_id):
    """Funtion to return JSON data for Genre"""
    tvseriesquery = session.query(Tvseries).filter_by(genre_id=genre_id).all()
    return jsonify(Tvseries=[i.serialize for i in tvseriesquery])


@app.route('/home/tvseries/<int:tvseries_id>/JSON')
def tvseriesJSON(tvseries_id):
    """Funtion to return JSON data for Genre"""
    tvseriesquery = session.query(Tvseries).filter_by(id=tvseries_id).one()
    return jsonify(tvseriesquery=tvseriesquery.serialize)


@app.route('/')
@app.route('/home')
def index():
    """"index page for the wesite """
    genrequery = session.query(Genre).all()
    tvseriesquery = session.query(Tvseries).order_by(
        desc(Tvseries.id)).limit(10).all()
    return render_template(
            'index.html', genres=genrequery, tvseries=tvseriesquery)


@app.route('/home/genre/<int:genre_id>/')
def genre(genre_id):
    """"genre page for the wesite """
    genrequery = session.query(Genre).filter_by(id=genre_id).one()
    tvseriesquery = session.query(Tvseries).filter_by(genre_id=genre_id).all()
    return render_template(
            'genre.html', genre=genrequery, tvseries=tvseriesquery)


@app.route('/home/tvseries/<int:tvseries_id>')
def tvseries(tvseries_id):
    """"genre page for the wesite """
    tvseriesquery = session.query(Tvseries).filter_by(id=tvseries_id).one()
    info = getUserInfo(restaurant.user_id)
    if 'username' not in login_session or info.id != login_session['user_id']:
        return render_template('tvseriespublic.html', tvseries=tvseriesquery)
    else:
        return render_template('tvseriesmembers.html', tvseries=tvseriesquery)


@app.route('/home/tvseries/add', methods=['GET', 'POST'])
def add_tvseries():
    """"page to add new tv series for the wesite"""
    if 'username' not in login_session:
        flash("login to Add new tvseries")
        return redirect('/login')
    if request.method == 'POST':
        newTvseries = Tvseries(
            name=request.form['name'],
            rating=request.form['rating'],
            description=request.form['description'],
            genre_id=request.form['genre_id'])
        session.add(newTvseries)
        flash("New Tvseries Successfully Added")
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('addtvseries.html')


@app.route('/home/tvseries/<int:tvseries_id>/edit', methods=['GET', 'POST'])
def edit_tvseries(tvseries_id):
    """"page to edit tv series for the wesite"""
    editedTvseries = session.query(Tvseries).filter_by(id=tvseries_id).one()
    if 'username' not in login_session:
        flash("login to edit the tvseries")
        return redirect('/login')
    if editedTvseries.user_id != login_session['user_id']:
        return """<script>function myFunction()
                {alert('you are not authorized to edit this tvseries');}
                </script><body onload='myFunction()''>"""
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
        return redirect(url_for('tvseries', tvseries_id=tvseries_id))
    else:
        return render_template('edittvseries.html', tvseries=editedTvseries)


@app.route('/home/tvseries/<int:tvseries_id>/delete', methods=['GET', 'POST'])
def delete_tvseries(tvseries_id):
    """"page to delete tv series for the wesite"""
    tvseriesDelete = session.query(Tvseries).filter_by(id=tvseries_id).one()
    if 'username' not in login_session:
        flash("login to delete the tvseries")
        return redirect('/login')
    if editedTvseries.user_id != login_session['user_id']:
        return """<script>function myFunction()
                {alert('you are not authorized to delete this tvseries');}
                </script><body onload='myFunction()''>"""
    if request.method == 'POST':
        session.delete(tvseriesDelete)
        flash("%s Successfully Deleted" % tvseriesDelete.name)
        session.commit
        return redirect(url_for('index'))
    else:
        return render_template('deletetvseries.html', tvseries=tvseriesDelete)


if __name__ == '__main__':
    app.secret_key = 'my_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5050)
