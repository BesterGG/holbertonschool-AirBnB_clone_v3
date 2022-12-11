#!/usr/bin/python3
"""
    Cities method files
"""
from api.v1.views.__init__ import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET', 'POST'])
def states_gen():
    """
        Method to retrieve or generate generic amenities object
    """
    req = request.get_json()
    if request.method == 'POST':
        status = 400 if not req or 'name' not in req else 201
        if not req:
            abort(status, 'Not a JSON')
        if 'name' not in req:
            abort(status, 'Missing name')
        obj = Amenity(**req)
        obj.save()
        return jsonify(obj.to_dict()), status
    if request.method == 'GET':
        obj_list = [am.to_dict() for am in storage.all("Amenity").values()]
        return jsonify(obj_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def states_scoped(amenity_id):
    """
        Method to retrieve/modify/delete a specific state object
    """
    met = request.method
    req = request.get_json()
    am = storage.get(Amenity, amenity_id)
    if am is None:
        abort(404)
    if met == 'GET':
        return jsonify(am.to_dict())
    if met == 'PUT':
        status = 404 if not req or 'name' not in req else 200
        if not req:
            abort(status, 'Not a JSON')
        if 'name' not in req:
            abort(status, 'Missing name')
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(am, key, value)
        storage.save()
        return jsonify(am), status
    if met == 'DELETE':
        storage.delete(am)
        storage.save()
        return {}, 200
