import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()

# Creating db table to hold all users
class User(Base):
	__tablename__ = 'user'

	# user table column names
	id = Column(Integer, primary_key=True)
	email = Column(String(250), nullable=False)
	name = Column(String(250), nullable=False)

	# Return as JSON object
	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'email': self.email
		}

# Creating db table for anime movie genres
class Genre(Base):
	__tablename__ = 'genre'

	# Table column names
	id = Column(Integer, primary_key=True)
	name = Column(String(200), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	# if selected genre is deleted, cascade will delete all the movies under that genre
	user = relationship(User, backref=backref('genres', uselist=True, cascade='delete, all'))

	# Return as JSON object
	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
		}


# Creating table for anime movies
class Movie(Base):
	__tablename__ = 'movie'

	# Table column names
	id = Column(Integer, primary_key=True)
	name = Column(String(200), nullable=False)
	description = Column(String(500))
	genre_id = Column(Integer, ForeignKey('genre.id'))
	genre = relationship(Genre, backref=backref('movies', uselist=True, cascade='delete, all'))
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User, backref=backref('movies', uselist=True, cascade='delete, all'))

	# Return as JSON object
	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
		}

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
