# !/usr/bin/env python

from flask import (Flask, render_template, request, redirect,
                    url_for, jsonify, session as login_session,
                    flash)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, User, Genre, Movie
from flask_oauth import OAuth
from urllib2 import Request, urlopen, URLError

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)

# Google login API
GOOGLE_CLIENT_ID = '955860244363-6oovigiiphjn9ph9epjq0hhe0bmrs4uc.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'yFzJFOqvB0UkEFm0uJxJKhkp'
REDIRECT_URL = '/google-oauth-callback'
SECRET_KEY = 'AIzaSyCTpECm-10n2XB09ydTKhRIIFj14P0FAFM'
DEBUG = True

app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()
google = oauth.remote_app(
    'google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                          'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SECRET)

# Create JSON object for all genres
@app.route('/genre/JSON')
def genreJSON():
	genre = session.query(Genre).all()
	return jsonify(genre=[g.serialize for g in genre])

# Create JSON object for Movies
@app.route('/movies/JSON')
def movieJSON():
	movie = session.query(Movie).all()
	return jsonify(movie=[m.serialize for m in movie])

# Creating route to access main home page
@app.route('/')
def load_main_page():
	all_genres = session.query(Genre).all()
	# if user already logged in then continue
	if ('name' in login_session):
		logged_in_name = login_session['name']
	else:
		logged_in_name = "Guest"
	return render_template('index.html',
                            genres=all_genres,
                            the_user_name=logged_in_name)

# Creating route to view movies under particular genre
@app.route('/genre/<genre_id>')
def view_movie_genres(genre_id):
	all_genres = session.query(Genre).all()
	current_genre = session.query(Genre).filter_by(id=genre_id).first()
	# query all movies under selected genre
	movies = session.query(Movie).filter_by(genre_id=genre_id).all()
	if ('name' in login_session):
		logged_in_name = login_session['name']
	else:
		logged_in_name = "Guest"
	return render_template('showMovies.html',genres=all_genres,movies=movies
						   ,genre=current_genre, the_user_name=logged_in_name)

# Creating route for accessing addGenre page to add a new movie genre
@app.route('/genre/add', methods=['GET', 'POST'])
def add_genre():
    if (request.method == 'POST'):	# post to database on form submit
        new_name = request.form['genre-name']	# get new genre name from the requested form
        new_genre = Genre(name=new_name, user_id=login_session['id'])
        session.add(new_genre)
        session.commit()
        return redirect(url_for('load_main_page', the_user_name=login_session['name']))
    else:
        # validating if user is logged in
        if ('name' in login_session):
            all_genres = session.query(Genre).all()
            logged_in_name = login_session['name']
            return render_template('addGenre.html',
                                    genres=all_genres,
                                    the_user_name=logged_in_name)
        # redirect user to the login page if not logged in
        else:
            return redirect(url_for('login'))

# Creating route to view added genres to delete
@app.route('/genre/delete')
def view_genres_to_delete():
    # validating if the user is logged in
	if ('name' in login_session):
		logged_in_name = login_session['name']
		deleted_genres = session.query(Genre).filter_by(user_id=login_session['id']).all()
		all_genres = session.query(Genre).all()
		return render_template('deleteGenre.html', genres=all_genres,
                                deleted=deleted_genres, the_user_name=logged_in_name)
	else:
		return redirect(url_for('login'))

# Creating route to delete anime movie genre
@app.route('/genre/<genre_id>/delete')
def delete_genre_now(genre_id):
    if ('name' in login_session):
        genre_delete = session.query(Genre).filter_by(id=genre_id).first()
        # validaing if genre_id belongs to the currently logged-in user
        if (genre_delete.user_id != login_session['id']):
            flash("You can only delete movie genres created by you!")
        else:
            session.delete(genre_delete)
            session.commit()
        return redirect(url_for('view_genres_to_delete', the_user_name=login_session['name']))
    else:
        return redirect(url_for('login'))

# Creating route to add new movies to the existing or new movie genre
@app.route('/genre/<genre_id>/add', methods=['GET', 'POST'])
def add_movie(genre_id):
    if (request.method == 'POST'):
        new_movie_name = request.form['movie-name']
        new_movie_description = request.form['movie-description']
        new_movie = Movie(name=new_movie_name,
                        description=new_movie_description,
                        genre_id=genre_id,
                        user_id=login_session['id'])
        session.add(new_movie)
        session.commit()
		# redirect to see all the movies under specified genre
        return redirect(url_for('view_movie_genres',
                        genre_id=genre_id,
                        genre_name=Genre.name,
                        the_user_name=login_session['name']))
    else:
        if ('name' in login_session):
            all_genres = session.query(Genre).all()
            genre = session.query(Genre).filter_by(id=genre_id).first()
            logged_in_name = login_session['name']
            return render_template('addMovie.html',
                                    genres=all_genres,
                                    genre=genre,
                                    the_user_name=logged_in_name)
        else:
            return redirect(url_for('login'))

# Creating route to edit added anime movies and their descriptions
@app.route('/genre/<genre_id>/<movie_id>/edit', methods=['GET', 'POST'])
def edit_movie(genre_id, movie_id):
    if (request.method == 'POST'):
        movie_to_edit = session.query(Movie).filter_by(id=movie_id).first()
        # validating if user created any movies
        if (movie_to_edit.user_id != login_session['id']):
            flash("You can only edit movies created by you!")
        else:
            new_name = request.form['movie-name']
            new_description = request.form['movie-description']
            movie_to_edit.name = new_name
            movie_to_edit.description = new_description
            session.add(movie_to_edit)
            session.commit()

        return redirect(url_for('view_movie_genres', genre_id=genre_id,
                        the_user_name=login_session['name']))
    else:
        if ('name' in login_session): # validating if the user is logged-in
            all_genres = session.query(Genre).all()
            genre = session.query(Genre).filter_by(id=genre_id).first()
            logged_in_name = login_session['name']
            movie_to_edit = session.query(Movie).filter_by(id=movie_id).first()
            return render_template('editMovie.html', genres=all_genres,
                                    movie=movie_to_edit, genre=genre,
                                    movie_id=movie_id, the_user_name=logged_in_name)
        else:
            return redirect(url_for('login'))

# Login Page button
@app.route('/login')
def login():
	callback=url_for('authorized', _external=True)
	return google.authorize(callback=callback)

# Logout Page button
@app.route('/logout')
def logout():
	# Release session variables
	login_session.pop('id', None)
	login_session.pop('name', None)
	return redirect(url_for('load_main_page'))

# Required Google authorization handler
@app.route(REDIRECT_URL)
@google.authorized_handler
def authorized(resp):
	access_token = resp['access_token']
	login_session['access_token'] = access_token, ''
	access_token = login_session.get('access_token')

	access_token = access_token[0]

	headers = {'Authorization': 'OAuth '+access_token}
	req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
	res = urlopen(req)
	# Parsing the response object to only get name and email
	arr = res.read().split(",")
	email_1 = arr[1].split(":")
	name_1 = arr[3].split(":")
	email = email_1[1].replace("\"", "")
	name = name_1[1].replace("\"", "")
	# Validating if the user already exists
	user = session.query(User).filter_by(email=email).first()
	if (user is None):	# If not, create new user Srecord
		u = User(name=name, email=email)
		session.add(u)
		session.commit()
		# Fetching user ID
		user = session.query(User).filter_by(email=email).first()
	# Setting session variables
	login_session['name'] = user.name
	login_session['id'] = user.id
    # Return to main page
	return redirect(url_for('load_main_page'))

# Required for the Google OAuth API
@google.tokengetter
def get_access_token():
    return login_session.get('access_token')

# Main method
if __name__ == '__main__':
	app.debug = False
	app.run(host='0.0.0.0', port=5000)
