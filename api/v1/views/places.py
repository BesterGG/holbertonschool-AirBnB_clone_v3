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
def cities_gen(city_id):
    """
        Method to retrieve or generate generic place object
    """
    met = request.method
    req = request.get_json()
    cities_list = [cit.to_dict() for cit in storage.all("City").values()]
    if city_id not in [cit['id'] for cit in cities_list]:
        abort(404)
    if met == "POST":
        if not req:
            abort(400, 'Not a JSON')
        if 'user_id' not in req:
            abort(400, 'Missing user_id')
        user_obj = storage.get(User, req_json.get('user_id'))
        if not user_obj:
            abort(400, 'Not a JSON')
        if 'name' not in req:
            abort(400, 'Missing name')
        req['city_id'] = city_id
        obj = Place(**req)
        obj.save()
        return jsonify(obj.to_dict()), 201
    if met == "GET":
        cities = storage.all("City")
        state_cities = [obj.to_dict() for obj in cities.values()
                        if obj.state_id == state_id]
        return jsonify(state_cities)


@app_views.route('/places/<place_id>', methods=["GET", "DELETE", "PUT"])
def amenities_scoped(place_id):
    """
        Method to retrieve/modify/delete a specific place object
    """
    met = request.method
    req = request.get_json()
    pl = storage.get(Place, place_id)
    if am is None:
        abort(404)
    if met == 'GET':
        return jsonify(am.to_dict())
    if met == 'PUT':
        status = 400 if not req or 'name' not in req else 200
        if not req:
            abort(status, 'Not a JSON')
        if 'name' not in req:
            abort(status, 'Missing name')
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(pl, key, value)
        storage.save()
        return jsonify(pl), status
    if met == 'DELETE':
        storage.delete(pl)
        storage.save()
        return {}, 200
