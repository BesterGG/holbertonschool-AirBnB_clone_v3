#!/usr/bin/python3
"""
    Place method files
"""
from api.v1.views.__init__ import app_views
from models import storage
from models.place import Place
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_gen(city_id):
    """
        Method to retrieve or generate generic place object
    """
    met = request.method
    req = request.get_json()
    obj_cities = [obj.to_dict() for obj in storage.all("City").values()]
    if city_id not in [cit['id'] for cit in obj_cities]:
        abort(404)
    if met == "GET":
        obj_places = storage.all("Place")
        obj_city_places = [obj.to_dict() for obj in obj_places.values()
                           if obj.city_id == city_id]
        return jsonify(obj_city_places)
    if met == "POST":
        if not req:
            abort(400, 'Not a JSON')
        if not req.get("user_id"):
            abort(400, "Missing user_id")
        user = storage.get(User, req.get("user_id"))
        if not user:
            abort(404, "Not found")
        if 'name' not in req:
            abort(400, 'Missing name')
        req["city_id"] = city_id
        new_place = Place(**req)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["GET", "DELETE", "PUT"])
def places_scoped(place_id):
    """
        Method to retrieve/modify/delete a specific place object
    """
    met = request.method
    req = request.get_json()
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    else:
        if met == "GET":
            return jsonify(obj_place.to_dict())
        if met == "DELETE":
            storage.delete(obj_place)
            storage.save()
            return {}, 200
        elif met == "PUT":
            if not req:
                abort(400, 'Not a JSON')
            for key, value in req.items():
                if key not in ['id', 'created_at',
                                'updated_at', 'city_id', 'user_id']:
                    setattr(obj_place, key, value)
            storage.save()
            return jsonify(obj_place.to_dict()), 200
