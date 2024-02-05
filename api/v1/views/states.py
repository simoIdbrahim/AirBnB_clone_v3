#!/usr/bin/python3
""" states page """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """ grab all """
    states = storage.all("State").values()
    list_of_states = [state.to_dict() for state in states]
    return jsonify(list_of_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ grab all """
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    return jsonify(the_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete state """
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    storage.delete(the_state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ create state """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    data = request.get_json()
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updates_state(state_id):
    """ update (PUT) state """
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    my_data = request.get_json()
    if my_data is None:
        return make_response("Not a JSON", 404)
    attributes = ['created_at', 'updated_at', 'id']
    for key, val in my_data.items():
        if key not in attributes:
            setattr(the_state, key, val)
    the_state.save()
    return jsonify(the_state.to_dict()), 200
