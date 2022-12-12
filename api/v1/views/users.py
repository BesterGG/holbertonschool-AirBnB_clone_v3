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
    """
        Method to retrieve/modify/delete a specific User object
    """
    if request.method == 'GET':
        return jsonify([obj.to_dict() for obj in
                        storage.all("User").values()])
    elif request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'email' not in request.get_json():
            abort(400, 'Missing email')
        if 'password' not in request.get_json():
            abort(400, 'Missing password')
        new_user = User(**request.get_json())
        new_user.save()
        return jsonify(new_user.to_dict()), 201



@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def users_scoped(user_id):
    """
        Method to retrieve/modify/delete a specific User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        if request.method == "GET":
            return jsonify(user.to_dict())
        if request.method == "DELETE":
            storage.delete(user)
            storage.save()
            return {}, 200
        elif request.method == "PUT":
            if not request.get_json():
                abort(400, 'Not a JSON')
            else:
                user = storage.get(User, user_id)
                for key, value in request.get_json().items():
                    if key not in ['id', 'created_at',
                                   'updated_at', 'email']:
                        setattr(user, key, value)
                storage.save()
                return jsonify(user.to_dict()), 200
