#!/usr/bin/python3
"""review places"""

from flask import jsonify, request, abort, make_response
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews_placees(place_id):
    """ load all places reviews  """
    my_place = storage.get(Place, place_id)
    if not my_place:
        abort(404)
    reviews = [review.to_dict() for review in my_place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def review(review_id):
    """ load one reviews by id"""
    my_review = storage.get(Review, review_id)
    if my_review is None:
        abort(404)
    return jsonify(my_review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ delete  reviews"""
    my_review = storage.get(Review, review_id)
    if my_review is None:
        abort(404)
    storage.delete(my_review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def add_reviews(place_id):
    """ create reviews """
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    my_data = request.get_json()
    if my_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "user_id" not in my_data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User, my_data["user_id"])
    if user is None:
        abort(404)
    if "text" not in my_data:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    my_data['place_id'] = place_id
    post_review = Review(**my_data)
    post_review.save()
    return make_response(jsonify(post_review.to_dict()), 201)


@app_views.route("reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_reviews(review_id):
    """ update  reviews """
    my_review = storage.get(Review, review_id)
    if my_review is None:
        abort(404)
    my_data = request.get_json()
    if my_data is None:
        return make_response("Not a JSON", 400)
    attributes = ["created_at", "updated_at", "id", "user_id",
                  "place_id"]
    for k, v in my_data.items():
        if k not in attributes:
            setattr(my_review, k, v)
    my_review.save()
    return jsonify(my_review.to_dict()), 200
