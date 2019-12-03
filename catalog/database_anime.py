# !/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Genre, Movie

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Method to add and commit to the db
def add_to_database(record):
    session.add(record)
    session.commit()

# Create admin user
admin = User(name='admin', email='admin@admin.com')
add_to_database(admin)

# Create some movie genres in the db
comedy = Genre(name='Comedy', user_id=1)
add_to_database(comedy)

romance = Genre(name='Romance', user_id=1)
add_to_database(romance)

drama = Genre(name='Drama', user_id=1)
add_to_database(drama)

horror = Genre(name='Horror', user_id=1)
add_to_database(horror)

# Add the movies to each created genres
movie = Movie(name='Gintama', description='Funny moments, hilarious scenes, wacky dialogue, comical happenings; all of these are covered by the comedy genre in anime', genre_id=1, user_id=1)
add_to_database(movie)

movie = Movie(name='Nichijou', description='The main purpose of the comedy genre is to make you laugh', genre_id=1, user_id=1)
add_to_database(movie)

movie = Movie(name='Toradora', description='The focus of these shows is the romantic relationships between the characters as well as their blooming love with one another', genre_id=2, user_id=1)
add_to_database(movie)

movie = Movie(name='Clannad', description='Drama anime tends to connect the viewers to the experiences of the characters', genre_id=3, user_id=1)
add_to_database(movie)

movie = Movie(name='Another', description='The most important factor for a show to be considered horror is its ability to scare and creep you out', genre_id=4, user_id=1)
add_to_database(movie)
