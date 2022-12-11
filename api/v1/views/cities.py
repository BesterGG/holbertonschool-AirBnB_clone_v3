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
        Method to retrieve or generate generic states object
    """
    met = request.method
    req = request.get_json()
    obj_list = [state.to_dict() for state in storage.all("State").values()]
    if state_id not in [state.get('id') for state in obj_list]:
        abort(404)
    if met == 'POST':
        status = 400 if not req or 'name' not in req else 201
        if not req:
            abort(status, 'Not a JSON')
        if 'name' not in req:
            abort(status, 'Missing name')
        req['state_id'] = state_id
        obj = City(**req)
        obj.save()
        return jsonify(obj.to_dict()), status
    if met == 'GET':
        obj_cities = storage.all('City')
        state_cities = [city.to_dict() for city in obj_cities.values()
                        if city.state_id == state_id]
        return jsonify(state_cities)


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def cities_scoped(city_id):
    """
        Method to retrieve/modify/delete a specific state object
    """
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)
    met = request.method
    req = request.get_json()
    if obj_city is None:
        abort(404)
    if met == 'GET':
        return jsonify(obj_city.to_dict())
    if met == 'PUT':
        status = 404 if not req or 'name' not in req else 200
        if not req:
            abort(status, 'Not a JSON')
        if 'name' not in req:
            abort(status, 'Missing name')
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj_city, key, value)
        storage.save()
        return jsonify(obj_city), status
    if met == 'DELETE':
        storage.delete(obj_city)
        storage.save()
        return {}, 200
