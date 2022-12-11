#!/usr/bin/python3
"""
    Cities method files
"""
from api.v1.views.__init__ import app_views
from models import storage
from models.city import City
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities_gen(state_id):
    """
        Method to retrieve or generate generic city object
    """
    met = request.method
    req = request.get_json()
    state_list = [obj.to_dict() for obj in storage.all("State").values()]
    ids = [obj['id'] for obj in state_list]
    if state_id not in ids:
        abort(404)
    if met == "POST":
        if not req:
            abort(400, 'Not a JSON')
        if 'name' not in req:
            abort(400, 'Missing name')
        req["state_id"] = state_id
        new_city = City(**req)
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    if met == "GET":
        cities = storage.all("City")
        state_cities = [obj.to_dict() for obj in cities.values()
                        if obj.state_id == state_id]
        return jsonify(state_cities)


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def cities_scoped(city_id):
    """
        Method to retrieve/modify/delete a specific city object
    """
    met = request.method
    req = request.get_json()
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)
    if met == "GET":
        return jsonify(obj_city.to_dict())
    if met == "PUT":
        if not req:
            abort(400, 'Not a JSON')
        if 'name' not in req:
            abort(400, 'Missing name')
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at', 'state_id']:
                setattr(obj_city, key, value)
        storage.save()
        return jsonify(obj_city.to_dict()), 200
    if met == "DELETE":
        storage.delete(obj_city)
        storage.save()
        return {}, 200
