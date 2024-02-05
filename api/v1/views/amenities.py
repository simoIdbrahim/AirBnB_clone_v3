#!/usr/bin/python3
"""  amenities api page """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """ load all amenities """
    amenities = storage.all("Amenity").values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ get amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ delte by id """
    amenitie = storage.get(Amenity, amenity_id)
    if amenitie is None:
        abort(404)
    storage.delete(amenitie)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """ POST amenity """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    may_data = request.get_json()
    amenity = Amenity(**may_data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ update (POST) amenity """
    amenitie = storage.get(Amenity, amenity_id)
    if amenitie is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    my_data = request.get_json()
    for k, val in my_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenitie, k, val)
    amenitie.save()
    return jsonify(amenitie.to_dict()), 200
