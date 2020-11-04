
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='show', lazy=False)


def __repr__(self):
      return f"<Venue id: {self.id}, name: {self.name}, shows {self.shows} >"
    # TODO: implement any missing fields, as a database migration using Flask-Migrate, Done


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='shows', lazy=False)


def __repr__(self):
      return f'<Artist id: {self.id}, name: {self.name}, genres: {self.genres}, image_link {self.image_link}, shows {self.shows} >'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate Done

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.Done


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)


def __repr__(self):
        return f'<Show {self.id} venue_id={venue_id} artist_id={artist_id} {self.start_time}>'
    # db.create_all()
