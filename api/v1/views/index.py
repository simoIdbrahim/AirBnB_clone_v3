#!/usr/bin/python3
""" flask index page """

from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ check app status its ok """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats')
def count():
    """ added count() method from storage """
    alls = {}
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"}
    for cls in classes:
        count = storage.count(cls)
        alls[classes.get(cls)] = count
    return jsonify(alls)
