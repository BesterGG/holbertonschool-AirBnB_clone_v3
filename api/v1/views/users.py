#!/usr/bin/python3
"""
    Users Blueprint files
"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET', 'POST'])
def users_gen():
    ''' Retrieves all users or adds a new one '''
    req = request.get_json()
    if request.method == 'POST':
        status = 400 if not req or 'name' not in req else 201
        if not req:
            abort(status, 'Not a JSON')
        if 'name' not in req:
            abort(status, 'Missing name')
        obj = User(**req)
        obj.save()
        return jsonify(obj.to_dict()), status
    if request.method == 'GET':
        obj_list = [user.to_dict() for user in storage.all("User").values()]
        return jsonify(obj_list)


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def users_scoped(user_id):
    """
        Method to retrieve/modify/delete a specific User object
    """
    met = request.method
    req = request.get_json()
    obj_list = [user.to_dict() for user in storage.all("User").values()]
    if user_id not in [user.get('id') for user in obj_list]:
        abort(404)
    if met == 'GET':
        for user in obj_list:
            if user.get('id') == user_id:
                return jsonify(user)
    if met == 'PUT':
        status = 404 if not req or 'name' not in req else 200
        if not req:
            abort(status, 'Not a JSON')
        if 'name' not in req:
            abort(status, 'Missing name')
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(storage.get(User, user_id), key, value)
        storage.save()
        return jsonify(storage.get(User, user_id)), status
    if met == 'DELETE':
        storage.delete(storage.get(User, user_id))
        storage.save()
        return {}, 200
