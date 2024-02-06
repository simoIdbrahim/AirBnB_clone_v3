#!/usr/bin/python3
""" Users  page """

from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ load or get all users """
    my_users = storage.all("User").values()
    my_users = [user.to_dict() for user in my_users]
    return jsonify(my_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ load user by id """
    my_user = storage.get(User, user_id)
    if my_user is None:
        abort(404)
    return jsonify(my_user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ removed user fron database """
    my_user = storage.get(User, user_id)
    if my_user is None:
        abort(404)
    storage.delete(my_user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """ post user """
    my_data = request.get_json()
    if my_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in my_data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in my_data:
        return make_response(jsonify({"error": "Missing password"}), 400)
    my_user = User(**my_data)
    my_user.save()
    return jsonify(my_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ updated  user """
    my_user = storage.get(User, user_id)
    if my_user is None:
        abort(404)
    my_data = request.get_json()
    if my_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, val in my_data.items():
        if k not in ["id", "email", "created_at", "updated_at"]:
            setattr(my_user, k, val)
    my_user.save()
    return jsonify(my_user.to_dict()), 200
