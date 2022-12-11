#!/usr/bin/python3
"""
    Comment
"""
from api.v1.views.__init__ import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def states_gen():
    """
        Method to retrieve or generate generic states object
    """
    req = request.get_json()
    if request.method == 'POST':
        status = 400 if not req or 'name' not in req else 201
        if not req:
            abort(status, 'Not a JSON')
        if 'name' not in req:
            abort(status, 'Missing name')
        obj = State(req)
        obj.save()
        return jsonify(obj.to_dict()), status
    if request.method == 'GET':
        obj_list = [state.to_dict() for state in storage.all("State").values()]
        return jsonify(obj_list)


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def states_scoped(state_id):
    """
        Method to retrieve/modify/delete a specific state object
    """
    met = request.method
    req = request.get_json()
    obj_list = [state.to_dict() for state in storage.all("State").values()]
    if state_id not in [state.get('id') for state in obj_list]:
        abort(404)
    if met == 'GET':
        for state in obj_list:
            if state.get('id') == state_id:
                return jsonify(state)
    if met == 'PUT':
        status = 404 if not req or 'name' not in req else 200
        if not req:
            abort(status, 'Not a JSON')
        if 'name' not in req:
            abort(status, 'Missing name')
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(storage.get(State, state_id), key, value)
        storage.save()
        return jsonify(storage.get(State, state_id)), status
    if met == 'DELETE':
        storage.delete(storage.get(State, state_id))
        storage.save()
        return {}, 200
