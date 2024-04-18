#!/usr/bin/python3
from flask import Flask
from flask import render_template
from flask import g
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
"""
Script that starts a Flask web application
"""
app = Flask(__name__)


@app.teardown_appcontext
def teardown_data(self):
        storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ return all states in the db  """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    return render_template('100-hbnb.html',
                           states=states,
                           places=places,
                           amenities=amenities)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
