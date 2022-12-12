#!/usr/bin/python3
''' Index python file '''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=["GET", "POST"])
def reviews_gen(place_id):
    """
        Method to retrieve or generate generic reviews object
    """
    met = request.method
    req = request.get_json()
    obj_places = [obj.to_dict() for obj in storage.all("Place").values()]
    if place_id not in [pl['id'] for pl in obj_places]:
        abort(404)
    if met == "GET":
        all_reviews = storage.all("Review")
        obj_reviews = [obj.to_dict() for obj in all_reviews.values()
                       if obj.place_id == place_id]
        return jsonify(obj_reviews)
    if met == "POST":
        if not req:
            abort(400, 'Not a JSON')
        if not req.get("user_id"):
            abort(400, "Missing user_id")
        obj_user = storage.get(User, req.get("user_id"))
        if not obj_user:
            abort(404, "Not found")
        if 'text' not in req:
            abort(400, 'Missing text')
        req["place_id"] = place_id
        obj = Review(**req)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["GET", "DELETE", "PUT"])
def reviews_scoped(review_id):
    """
        Method to retrieve/modify/delete a specific reviews object
    """
    met = request.method
    req = request.get_json()
    obj_review = storage.get(Review, review_id)
    if obj_review is None:
        abort(404)
    if met == "GET":
        return jsonify(obj_review.to_dict())
    if met == "DELETE":
        storage.delete(obj_review)
        storage.save()
        return {}, 200
    if met == "PUT":
        if not req:
            abort(400, 'Not a JSON')
        for key, value in req.items():
            if key not in ['id', 'created_at',
                           'updated_at', 'place_id', 'user_id']:
                setattr(obj_review, key, value)
        storage.save()
        return jsonify(obj_review.to_dict()), 200
