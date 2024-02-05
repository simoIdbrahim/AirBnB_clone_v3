#!/usr/bin/python3
""" city page """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def list_cities(state_id):
    """" get all citys """
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    citys = [city.to_dict() for city in the_state.citys]
    return jsonify(citys)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """" get all citys """
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    return jsonify(the_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """" delete citys """
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    storage.delete(the_city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """" create citys """
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    my_data = request.get_json()
    my_data['state_id'] = state_id
    new_city = City(**my_data)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """" update (PUT) citys """
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    my_data = request.get_json()
    if my_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in my_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(the_city, key, value)
    the_city.save()
    return jsonify(the_city.to_dict()), 200
