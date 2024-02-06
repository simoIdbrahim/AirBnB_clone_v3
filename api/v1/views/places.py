#!/usr/bin/python3
"""Places view module"""

from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ load or get all places in city """
    my_city = storage.get(City, city_id)
    if my_city is None:
        abort(404)
    places = [place.to_dict() for place in my_city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ load one place in city """
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    return jsonify(my_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ delete place"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    storage.delete(my_place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ create place"""
    my_city = storage.get(City, city_id)
    if my_city is None:
        abort(404)
    my_data = request.get_json()
    if not my_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in my_data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    the_user = storage.get(User, my_data["user_id"])
    if the_user is None:
        abort(404)
    if 'name' not in my_data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    my_data['city_id'] = city_id
    my_place = Place(**my_data)
    my_place.save()
    return make_response(jsonify(my_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ update all place """
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    my_data = request.get_json()
    if my_data is None:
        return make_response('Not a JSON', 400)
    for k, val in my_data.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(my_place, k, val)
    my_place.save()
    return make_response(jsonify(my_place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """ find all places"""
    if request.get_json() is not None:
        params = request.get_json()
        states = params.get(State, [])
        cities = params.get(City, [])
        amenities = params.get('amenities', [])
        amen_objs = []
        for amen_id in amenities:
            amenity = storage.get(Amenity, amen_id)
            if amenity:
                amen_objs.append(amenity)
        if states == cities == []:
            places = storage.all('Place').values()
        else:
            all_places = []
            for state_id in states:
                state = storage.get(State, state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get(City, city_id)
                for place in city.all_places:
                    all_places.append(place)
        confirmed_places = []
        for place in all_places:
            place_amenities = place.amenities
            confirmed_places.append(place.to_dict())
            for amenity in amen_objs:
                if amenity not in place_amenities:
                    confirmed_places.pop()
                    break
        return jsonify(confirmed_places)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

