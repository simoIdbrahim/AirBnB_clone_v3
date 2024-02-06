#!/usr/bin/python3
""" palce amenities """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
import os


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_(place_id):
    """ load amenities placres """
    my_place = storage.get("Place", place_id)
    if my_place is None:
        abort(404)
    amenities = []
    for amenity in my_place.amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_(place_id, amenity_id):
    """ deletes amenity"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in my_place.amenities:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        my_place.amenities.remove(amenity)
    else:
        my_place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_amenity_(place_id, amenity_id):
    """ related a Amenity to a Place"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    if amen in my_place.amenities:
        return jsonify(amen.to_dict()), 200
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        my_place.amenities.append(amen)
    else:
        my_place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amen.to_dict()), 201


@app_views.route('/places/<place_id>/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity_by_place_(place_id):
    """ post amenity"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    my_data = request.get_json()
    amenity = Amenity(**my_data)
    amenity.save()
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        my_place.amenities.append(amenity)
    else:
        my_place.amenity_ids.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_place_(place_id, amenity_id):
    """ deletes amenity """
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in my_place.amenities:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        my_place.amenities.remove(amenity)
    else:
        my_place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200
