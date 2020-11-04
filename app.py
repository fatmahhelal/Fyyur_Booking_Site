#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
from flask import (
    Flask, 
    render_template, 
    request, 
    Response, 
    flash, 
    redirect, 
    url_for
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from flask_migrate import Migrate
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database, Done
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format = "EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format = "EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
# TODO:Done
@app.route('/venues')
def venues():     

 venues = Venue.query.all()
 data = []
 for place in Venue.query.distinct(Venue.city, Venue.state).all():
    data.append({
        'city': place.city,
        'state': place.state,
        'venues': [{
            'id': venue.id,
            'name': venue.name,
        } for venue in venues if
            venue.city == place.city and venue.state == place.state]
    })
 return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee" Done
  search_term = request.form.get('search_term', '')
  search_venue = "%{}%".format(search_term)
  search_reasult = Venue.query.filter(Venue.name.like(search_venue)).all()
  response = {
    "count": len(search_reasult),
    "data": search_reasult
    }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

# TODO: Done
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
 
  upcoming_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id, Show.artist_id==Artist.id, Show.start_time>datetime.now()).all()
  upcoming_shows = []
  for show in upcoming_shows_query:
    upcoming_shows.append({
            "artist_id": show.artist_id,
            "artist_name": db.session.query(Artist.name).filter_by(id=show.artist_id).first()[0],
            "artist_image_link": db.session.query(Artist.image_link).filter_by(id=show.artist_id).first()[0],
            "start_time": str(show.start_time)   
    })

  past_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id, Show.artist_id==Artist.id, Show.start_time<datetime.now()).all()
  past_shows = []
  for show in past_shows_query:
    past_shows.append({
            "artist_id": show.artist_id,
            "artist_name": db.session.query(Artist.name).filter_by(id=show.artist_id).first()[0],
            "artist_image_link": db.session.query(Artist.image_link).filter_by(id=show.artist_id).first()[0],
            "start_time": str(show.start_time)
    })

  data = {
    "id": venue.id,
    "name": venue.name,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "facebook_link": venue.facebook_link,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
   # error = False
  # TODO: insert form data as a new Venue record in the db, instead, Done
  try:
        name = request.form['name'],
        city = request.form['city'],
        state = request.form['state'],
        address = request.form['address'],
        phone = request.form['phone'],
        image_link=request.form['image_link'],
        facebook_link = request.form['facebook_link'],
        #shows=request.form['shows'],
    # TODO: modify data to be the data object returned from db insertion Done

        venue = Venue(
        name=name,
        city=city,
        state=state,
        address=address,
        phone=phone,
        image_link=image_link,
        facebook_link=facebook_link,
        # shows=request.form['shows'],
        )

        db.session.add(venue)
        db.session.commit()
       # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    # TODO: on unsuccessful db insert, flash an error instead. Done
        db.session.rollback()
        flash('An error occurred, Venue ' + request.form['name'] + ' was unsuccessful listed!')
  finally:
        db.session.close()
  return render_template('pages/home.html')



#need fix
@ app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.Done
    error = False
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully DELETE!')
    except():
        db.session.rollback()
        error = True
        flash('Venue ' + request.form['name'] + ' was Unsuccessfully DELETE!')
    finally:
        db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    return jsonify({'success': True})


#  Artists 
#  ----------------------------------------------------------------

#need Done
@ app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database Done
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)


@ app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band". Done
 search_term = request.form.get('search_term', '')
 search_artist = "%{}%".format(search_term)
 search_reasult = Artist.query.filter(Artist.name.like(search_artist)).all()
 response = {
    "count": len(search_reasult),
    "data": search_reasult
    }
 return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id Done
  
  artist = Artist.query.get(artist_id)
  
  upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==Venue.id, Show.artist_id==artist_id, Show.start_time>datetime.now())
  upcoming_shows = []
  for show in upcoming_shows_query:
    upcoming_shows.append({
            "venue_id": show.venue_id,
            "venue_name": db.session.query(Venue.name).filter_by(id=show.venue_id).first()[0],
            "venue_image_link": db.session.query(Venue.image_link).filter_by(id=show.venue_id).first()[0],
            "start_time": str(show.start_time)   
    })

  past_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==Venue.id, Show.artist_id==artist_id, Show.start_time<datetime.now())
  past_shows = []
  for show in past_shows_query:
    past_shows.append({
            "venue_id": show.venue_id,
            "venue_name": db.session.query(Venue.name).filter_by(id=show.venue_id).first()[0],
            "venue_image_link": db.session.query(Venue.image_link).filter_by(id=show.venue_id).first()[0],
            "start_time": str(show.start_time)
    })

  data = {
    "id": artist.id,
    "name": artist.name,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(
    name = artist.name,
    city = artist.city,
    state = artist.state,
    genres = artist.genres,
    phone = artist.phone,
    image_link = artist.image_link,
    facebook_link = artist.facebook_link,
  )
  # TODO: populate form with fields from artist with ID <artist_id> Done
  return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = None
    artist = Artist.query.get(artist_id)
  # TODO: take values from the form submitted, and update existing Done
    try:
        artist.name = request.form['name'],
        artist.city = request.form['city'],
        artist.state = request.form['state'],
        artist.genres =json.dumps (request.form['genres']),
        artist.phone = request.form['phone'],
        artist.image_link=request.form['image_link'],
        artist.facebook_link = request.form['facebook_link'],
        db.session.update(artist)
        db.session.commit()
       # on successful db Update, flash success
        flash('Artist ' + request.form['name'] + ' was successfully Update!')
    except():
    # TODO: on unsuccessful db Update, flash an error instead. Done
        db.session.rollback()
        flash('An error occurred, Artist ' + request.form['name'] + ' was unsuccessful Update!')
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
    venue = Venue.query.get(venue_id)
    form = VenueForm(
    name = venue.name,
    city = venue.city,
    state = venue.state,
    address = venue. address,
    phone = venue.phone,
    image_link = venue.image_link,
    facebook_link = venue.facebook_link,
  )
  # TODO: populate form with values from venue with ID <venue_id> Done
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
   error = None
   venue = Venue.query.get(venue_id)
   try:
        venue.name = request.form['name'],
        venue.city = request.form['city'],
        venue.state = request.form['state'],
        venue.address = request.form['address'],
        venue.phone = request.form['phone'],
        venue.image_link=request.form['image_link'],
        venue.facebook_link = request.form['facebook_link'],
        db.session.update(venue)
        db.session.commit()
       # on successful db Update, flash success
        flash('Venue ' + request.form['name'] + ' was successfully Update!')
   except():
    # TODO: on unsuccessful db Update, flash an error instead. Done
        db.session.rollback()
        flash('An error occurred, Venue ' + request.form['name'] + ' was unsuccessful Update!')
   finally:
        db.session.close()
   return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new artists record in the db, instead Done
  # TODO: modify data to be the data object returned from db insertion Done
    try:
        name = request.form['name'],
        city = request.form['city'],
        state = request.form['state'],
        genres =json.dumps (request.form['genres']),
        phone = request.form['phone'],
        image_link=request.form['image_link'],
        facebook_link = request.form['facebook_link'],
        # shows=request.form['shows'],
        artist = Artist(
        name=name,
        city=city,
        state=state,
        #address=address,
        phone=phone,
        genres=genres,
        image_link=image_link,
        facebook_link=facebook_link,
        # shows=request.form['shows'],
        )

        db.session.add(artist)
        db.session.commit()
       # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
    # TODO: on unsuccessful db insert, flash an error instead. Done
        db.session.rollback()
        flash('An error occurred, Artist ' + request.form['name'] + ' was unsuccessful listed!')
    finally:
        db.session.close()
    return render_template('pages/home.html')

  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')




#  Shows
#  ----------------------------------------------------------------
# done
@app.route('/shows')
def shows():
    shows = Show.query.all()
    data = []
    for show in shows:
        data.append({
            "start_time": str(show.start_time),
            "venue_id": show.venue_id,
            "artist_id": show.artist_id,
            #pring data by refrence to join table
            "venue_name": db.session.query(Venue.name).filter_by(id=show.venue_id).first()[0],
            "artist_name": db.session.query(Artist.name).filter_by(id=show.artist_id).first()[0],
            "artist_image_link": db.session.query(Artist.image_link).filter_by(id=show.artist_id).first()[0],
        })

    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()
  try:
        venue_id = request.form['venue_id'],
        artist_id = request.form['artist_id'],
        start_time = request.form['start_time'],

        # shows=request.form['shows'],
        show = Show(
        venue_id=venue_id,
        artist_id=artist_id,
        start_time=start_time,
        )

        db.session.add(show)
        db.session.commit()
       # on successful db insert, flash success
        flash('Show was successfully listed!')
        return render_template('pages/home.html')

  except Exception as e:
    # TODO: on unsuccessful db insert, flash an error instead. Done
        flash('Show was unsuccessfully listed!')
        db.session.rollback()
        return render_template('forms/new_show.html', form=form)
  finally:
        db.session.close()   

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
