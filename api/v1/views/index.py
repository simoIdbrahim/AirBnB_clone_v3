#!/usr/bin/python3
''' create a route '''


from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def api_status():
    """ return res json """
    res = {'status': 'OK'}
    return jsonify(res)


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """ find num obj by type"""
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
